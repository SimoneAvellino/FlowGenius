const { EMURGenerator } = require('./emur');

const generator = new EMURGenerator(process.env.EMUR_FLOW_YEAR, process.env.EMUR_FLOW_FILE_TYPE);

module.exports.start_simulation = async (req, res) => {
    generator.run();
    res.status(200).send('Simulation started');
}
module.exports.stop_simulation = async (req, res) => {
    generator.stop();
    res.status(200).send('Simulation stopped');
}
