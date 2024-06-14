from utility.client_simulation.emur import EMUR_generator
import pandas as pd
import time

def access_json(json_data, keys):
    try:
        value = json_data
        for key in keys:
            value = value[key]
        return value
    except (KeyError, TypeError):
        return None

generator = EMUR_generator(file_path="../producer/logic/emur/data/2023.xml", file_type="XML", seconds_for_interval=1)
df = pd.DataFrame(columns=['data', 'modalita_arrivo', 'responsabile_invio', 'problema_principale', 'triage', 'data_nascita', 'genere', 'cittadinanza', 'comune_residenza', 'diagnosi_principale', 'prestazione_principale', 'esito_trattamento', 'costo_lordo'])

while True:
    record = generator.next()
    if record is None:
        break

    # print(record)

    data = access_json(record, ['Entrata', 'ns0:Data']) + ' ' + access_json(record, ['Entrata', 'ns0:Ora'])
    modalita_arrivo = access_json(record, ['ModalitaArrivo'])
    responsabile_invio = access_json(record, ['ResponsabileInvio'])
    problema_principale = access_json(record, ['ProblemaPrincipale'])
    triage = access_json(record, ['Triage'])
    anno_nascita = access_json(record, ['Assistito', 'ns0:DatiAnagrafici', 'ns0:Eta', 'ns0:Nascita', 'ns0:Anno'])
    mese_nascita = access_json(record, ['Assistito', 'ns0:DatiAnagrafici', 'ns0:Eta', 'ns0:Nascita', 'ns0:Mese'])
    if anno_nascita and mese_nascita:
        data_nascita = anno_nascita + '/' + mese_nascita + '/01'
    else:
        data_nascita = None
    genere = access_json(record, ['Assistito', 'ns0:DatiAnagrafici', 'ns0:Genere'])
    cittadinanza = access_json(record, ['Assistito', 'ns0:DatiAnagrafici', 'ns0:Cittadinanza'])
    comune_residenza = access_json(record, ['Assistito', 'ns0:DatiAnagrafici', 'ns0:Residenza', 'ns0:Comune'])
    diagnosi_principale = access_json(record, ['Assistito', 'ns0:Prestazioni', 'ns0:Diagnosi', 'ns0:DiagnosiPrincipale'])
    prestazione_principale = access_json(record, ['Assistito', 'ns0:Prestazioni', 'ns0:Prestazione', 'ns0:PrestazionePrincipale'])
    esito_trattamento = access_json(record, ['Assistito', 'ns0:Dimissione', 'ns0:EsitoTrattamento'])
    costo_lordo = access_json(record, ['Importo', 'ns0:Lordo'])

    df.loc[len(df)] = [data, modalita_arrivo, responsabile_invio, problema_principale, triage, data_nascita, genere, cittadinanza, comune_residenza, diagnosi_principale, prestazione_principale, esito_trattamento, costo_lordo]


df.to_csv("./2023.csv", index=False)