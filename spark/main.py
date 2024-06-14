from pyspark.sql import SparkSession
from pyspark.sql.functions import col
from pyspark.conf import SparkConf
from schema import format_df
from es_daily_query import daily_problems, notify_problems, delete_predictions
from model import predict_problems
import pandas as pd
from datetime import timedelta

sparkConf = SparkConf().set("es.nodes", "elasticsearch") \
    .set("es.port", "9200")

spark = SparkSession.builder.appName("hospital_flow_analyzer").config(conf=sparkConf).getOrCreate()

spark.sparkContext.setLogLevel("ERROR")

df = spark \
    .readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "kafka:9092") \
    .option("subscribe", "emur") \
    .load()

df = format_df(df)


# Write to Elasticsearch
es_stream = df.writeStream \
    .option("checkpointLocation", "/tmp/") \
    .format("es") \
    .start("emur_flow")

# Write to console (for debugging)
# console_stream = df \
#     .writeStream \
#     .outputMode("append") \
#     .format("console") \
#     .start()


#######################################################
# data enrichment

# everytime a new batch is processed, we want to run the query
# if the column "datetime" contains the date we are interested in
# we want to run the query

yesterday_date = None
predict_df = None
context_length = 8

def process_batch(batch_df, batch_id):

    global yesterday_date
    global predict_df
    global context_length

    try :

        today_date = batch_df.select("datetime").orderBy(col("datetime").desc()).first()[0].date()
        tomorrow_date = today_date + timedelta(days=1)

        # the first time we run the process_batch we don't have a yesterday_date
        if yesterday_date is None:
            yesterday_date = today_date
            predict_df = pd.read_csv("/opt/bitnami/spark/scripts/data/start_time_series.csv", parse_dates=["date"]).iloc[-context_length:]
            predict_df = predict_df.drop(columns=["date"])

            return
        elif yesterday_date != today_date:
            ######
            # get the problems of yesterday
            yesterday_problems = daily_problems(yesterday_date)
            #######
            # predict problems
            context_length = 8
            # access the second element of the tuple because is the prediction of tomorrow
            # because the prediction is made on the data up to tomorrow

            # past_data, yesterday, today, tomorrow
            # use of past_data and yesterday to predict tomorrow because we don't have all the data of today
            tomorrow_problems = predict_problems(predict_df)[1]
            #######
            # send yesterday_problems to elasticsearch
            notify_problems(tomorrow_problems, tomorrow_date)
            # delete the predictions of yesterday
            delete_predictions(yesterday_date)
            # update with the actual data
            notify_problems(yesterday_problems, yesterday_date)
            #######
            # update the dataframe for prediction
            predict_df.loc[len(predict_df)] = yesterday_problems
            # remove the first row
            predict_df = predict_df.iloc[1:].reset_index(drop=True)
            predict_df = predict_df.copy()
            yesterday_date = today_date

    except Exception as e:
        print("Error in process_batch", e)


df.writeStream.foreachBatch(process_batch).start()

#######################################################

es_stream.awaitTermination()
# console_stream.awaitTermination()
