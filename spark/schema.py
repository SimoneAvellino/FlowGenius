from pyspark.sql.types import StructType, StructField, StringType, FloatType, MapType
from pyspark.sql.functions import col, from_json, concat_ws, expr

schema = StructType([
    StructField("Identificativo", StringType(), True),
    StructField("Erogatore", StructType([
        StructField("CodiceIstituto", StringType(), True)
    ]), True),
    StructField("Entrata", StructType([
        StructField("Data", StringType(), True),
        StructField("Ora", StringType(), True)
    ]), True),
    StructField("ModalitaArrivo", StringType(), True),
    StructField("ResponsabileInvio", StringType(), True),
    StructField("ProblemaPrincipale", StringType(), True),
    StructField("DiagnosiPrincipale", StringType(), True),
    StructField("PrestazionePrincipale", StringType(), True),
    StructField("Triage", StringType(), True),
    StructField("Assistito", StructType([
        StructField("CUNI", StringType(), True),
        StructField("ValiditaCI", StringType(), True),
        StructField("TipologiaCI", StringType(), True),
        StructField("CodiceIstituzioneTEAM", StringType(), True),
        StructField("DatiAnagrafici", StructType([
            StructField("Eta", StructType([
                StructField("Nascita", StructType([
                    StructField("Anno", StringType(), True),
                    StructField("Mese", StringType(), True)
                ]), True),
            ]), True),
            StructField("Genere", StringType(), True),
            StructField("Cittadinanza", StringType(), True),
            StructField("Residenza", MapType(StringType(), StringType()), True)
        ]), True),
        StructField("Prestazioni", StructType([
            StructField("PresaInCarico", MapType(StringType(), StringType()), True),
            StructField("Diagnosi", MapType(StringType(), StringType()), True),
            StructField("Prestazione", MapType(StringType(), StringType()), True)
        ]), True),
        StructField("Dimissione", StructType([
            StructField("EsitoTrattamento", StringType(), True),
            StructField("Data", StringType(), True),
            StructField("Ora", StringType(), True),
            StructField("LivelloAppropriatezzaAccesso", StringType(), True)
        ]), True)
    ]), True),
    StructField("Importo", StructType([
        StructField("RegimeErogazione", StringType(), True),
        StructField("Lordo", StringType(), True),  # Rimane come stringa
        StructField("PosizioneAssistitoTicket", StringType(), True)
    ]), True),
    StructField("TipoTrasmissione", StringType(), True)
])

def format_df(df):
    return df.selectExpr("CAST(value AS STRING) as json") \
    .select(from_json("json", schema).alias("data")) \
    .select(
        col("data.Identificativo"),
        col("data.Erogatore.CodiceIstituto"),
        concat_ws(" ", col("data.Entrata.Data"), col("data.Entrata.Ora")).cast("timestamp").alias("datetime"),
        col("data.ModalitaArrivo"),
        col("data.ResponsabileInvio"),
        col("data.ProblemaPrincipale"),
        col("data.DiagnosiPrincipale"),
        col("data.PrestazionePrincipale"),
        col("data.Triage"),
        col("data.Assistito.DatiAnagrafici.Eta.Nascita.Mese").cast("int").alias("MeseNascita"),
        col("data.Assistito.DatiAnagrafici.Eta.Nascita.Anno").cast("int").alias("AnnoNascita"),
        col("data.Assistito.DatiAnagrafici.Genere").alias("Genere"),
        col("data.Assistito.DatiAnagrafici.Cittadinanza").alias("Cittadinanza"),
        expr("data.Assistito.DatiAnagrafici.Residenza['Comune']").alias("Residenza"),
        expr("data.Assistito.Prestazioni.Diagnosi['DiagnosiPrincipale']").alias("Diagnosi"),
        col("data.Assistito.Dimissione.EsitoTrattamento"),
        col("data.Importo.Lordo").cast(FloatType()).alias("prezzo_lordo"),
        col("data.TipoTrasmissione")
    )