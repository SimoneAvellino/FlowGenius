# Analisi dei Flussi EMUR

Questo progetto implementa una pipeline di elaborazione dati per l'analisi dei flussi EMUR (Emergenza Urgenza) utilizzando una serie di strumenti containerizzati tramite Docker. La pipeline è composta da vari servizi tra cui un produttore di dati, un broker di messaggi, un motore di elaborazione dati, e un sistema di visualizzazione.

## Descrizione del Progetto

L'obiettivo del progetto è di simulare e analizzare i flussi di dati EMUR per il Policlinico di Messina. Il progetto utilizza un'architettura basata su microservizi, dove ogni componente svolge un ruolo specifico nella raccolta, elaborazione e visualizzazione dei dati. La peculiarità del modello è l'uso di TimeSeries per prevedere i problemi principali dell'indomani.

## Architettura della Pipeline

1. **Producer**: Simula la produzione di flussi di dati EMUR e invia i dati a Fluentd.
2. **Fluentd**: Sistema di logging per la raccolta e l'invio dei dati a Kafka.
3. **Zookeeper**: Coordinatore per il cluster di Kafka.
4. **Kafka**: Broker di messaggi per la gestione dei flussi di dati.
5. **Spark**: Motore di elaborazione dei dati, che processa i dati provenienti da Kafka e li invia a Elasticsearch.
6. **Elasticsearch**: Sistema di ricerca e indicizzazione per l'archiviazione dei dati.
7. **Kibana**: Strumento di visualizzazione dei dati indicizzati in Elasticsearch.

## Installazione

Per avviare la pipeline, segui questi passaggi:

1. Clona il repository.
2. Costruisci e avvia i container Docker utilizzando `docker-compose`.

I dati per ora non sono pubblici in quanto sono dell'ospedale. In futuro, potrebbero essere pubblicati dati fittizi per provare il modello.

## Uso

Una volta che la pipeline è in esecuzione, i dati EMUR simulati dal produttore verranno raccolti da Fluentd, inviati a Kafka, elaborati da Spark e indicizzati in Elasticsearch. Kibana può essere utilizzato per visualizzare e analizzare questi dati.

## Contatti

Per ulteriori domande o supporto, contatta:

- Nome: Simone Avellino
- Email: s.avellino02@gmail.com
- Instagram: @simoneavellinoo
- GitHub: https://github.com/SimoneAvellino
