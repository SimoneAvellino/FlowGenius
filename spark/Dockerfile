# Usa un'immagine di base di Spark
FROM bitnami/spark:3.4.2

# Passa all'utente root per eseguire i comandi di installazione
USER root

# Aggiorna il package list e installa GCC
RUN mkdir -p /var/lib/apt/lists/partial && apt-get clean && apt-get update && apt-get install -y gcc

# Installa le librerie Python necessarie
RUN pip install elasticsearch pandas torch transformers[torch]






# Copia i file di script nella directory di lavoro del container
COPY ./spark /opt/bitnami/spark/scripts

# Rendi eseguibile lo script principale
RUN chmod +x /opt/bitnami/spark/scripts/main.py
