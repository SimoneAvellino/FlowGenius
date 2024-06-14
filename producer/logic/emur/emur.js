const fs = require('fs');
const path = require('path');
const xml2js = require('xml2js');
const axios = require('axios');

class XMLReader {
    constructor(file_path) {
        this.file_path = file_path;
        this.data = null;
        this.current_index = 0;
    }

    async parseXML() {
        const xmlString = fs.readFileSync(this.file_path, 'utf-8');
        const parser = new xml2js.Parser({
            explicitArray: false,
            mergeAttrs: true
        });
        return new Promise((resolve, reject) => {
            parser.parseString(xmlString, (err, result) => {
                if (err) reject(err);
                resolve(result);
            });
        });
    }

    async initialize() {
        const data = await this.parseXML();
        this.data = data.flsProSoc.item;
    }

    flow_type() {
        return 'XML';
    }


    async next() {
        if (!this.data || this.current_index >= this.data.length) return null;
    
        const item = this.data[this.current_index++];

        return item;

    }
}

class EMURGenerator {
    constructor(year, file_type, seconds_for_interval = 0.2) {
        if (file_type !== 'xml') throw new Error('Unsupported file type');
        const filePath = path.resolve(__dirname, 'data', `${year}.xml`);
        this.flow_reader = new XMLReader(filePath);
        this.seconds_for_interval = seconds_for_interval;
        this.started = false;
    }

    async run() {
        this.started = true;
        await this.flow_reader.initialize();
        while (this.started) {
            const record = await this.flow_reader.next();
            if (!record) break;
            await this.formatRecord(record);
            await this.pubblish(record);
            await new Promise(resolve => setTimeout(resolve, this.seconds_for_interval * 1000));
        }
    }

    async formatRecord(record) {

        try {
            record['Assistito']['DatiAnagrafici']['DataNascita'] = new Date(
                record['Assistito']['DatiAnagrafici']['Eta']['Nascita']['Anno'],
                record['Assistito']['DatiAnagrafici']['Eta']['Nascita']['Mese'] - 1
            );
        } catch (error) {
            record['Assistito']['DatiAnagrafici']['DataNascita'] = null;
        }
        

        if (record['Assistito']['Prestazioni']['Diagnosi'] != "") {
            record['DiagnosiPrincipale'] = record['Assistito']['Prestazioni']['Diagnosi']['DiagnosiPrincipale'];
        } else {
            record['DiagnosiPrincipale'] = null;
        }

        if (record['Assistito']['Prestazioni']['Diagnosi'] != "") {
            record['DiagnosiPrincipale'] = record['Assistito']['Prestazioni']['Diagnosi']['DiagnosiPrincipale'];
        } else {
            record['DiagnosiPrincipale'] = null;
        }

        if (record['Assistito']['Prestazioni']['Prestazione'] != "") {
            record['PrestazionePrincipale'] = record['Assistito']['Prestazioni']['Prestazione']['PrestazionePrincipale'];
        } else {
            record['PrestazionePrincipale'] = "";
        }

        // if (record['Assistito']['Prestazioni']['Prestazione']) {

        // }

        

        // // convert the array of prestazioneSecondaria and diagnosiSecondaria to array if it is not
        // if (record['Assistito']['Prestazioni']['Prestazione']['PrestazioneSecondaria'] && !Array.isArray(record['Assistito']['Prestazioni']['Prestazione']['PrestazioneSecondaria'])) {
        //     record['Assistito']['Prestazioni']['Prestazione']['PrestazioneSecondaria'] = [record['Assistito']['Prestazioni']['Prestazione']['PrestazioneSecondaria']];
        // } else if(!record['Assistito']['Prestazioni']['Prestazione']['PrestazioneSecondaria']) {
        //     record['Assistito']['Prestazioni']['Prestazione']['PrestazioneSecondaria'] = [];
        // }

        // // convert the array of diagnosiSecondaria to array if it is not
        // if (record['Assistito']['Prestazioni']['Diagnosi']['DiagnosiSecondaria'] && !Array.isArray(record['Assistito']['Prestazioni']['Diagnosi']['DiagnosiSecondaria'])) {
        //     record['Assistito']['Prestazioni']['Diagnosi']['DiagnosiSecondaria'] = [record['Assistito']['Prestazioni']['Diagnosi']['DiagnosiSecondaria']];
        // } else if(!record['Assistito']['Prestazioni']['Diagnosi']['DiagnosiSecondaria']) {
        //     record['Assistito']['Prestazioni']['Diagnosi']['DiagnosiSecondaria'] = [];
        // }
        
        return record;
    }

    async pubblish(record) {
        try {
            await axios.post(`http://${process.env.FLUENTD_HOST}:${process.env.FLUENTD_PORT}/${process.env.FLOW_TYPE}`, record, {
                headers: {
                    'Content-Type': 'application/json'
                }
            });
        } catch (error) {
            console.error('Error publishing to Fluentd:', error);
        }
    }


    async stop() {
        this.started = false;
    }
}

module.exports.EMURGenerator = EMURGenerator;