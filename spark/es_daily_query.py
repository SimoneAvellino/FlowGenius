from io import StringIO

from elasticsearch import Elasticsearch
import pandas as pd
from datetime import datetime



def daily_problems(date):
    """
    Run a query on Elasticsearch to get the daily problems. (from the emur_flow index)
    The query will return the number of occurrences of each problem for the given date.
    """

    # elastic has timestamp in milliseconds
    start_timestamp = datetime.strptime(str(date), "%Y-%m-%d").timestamp() * 1000
    end_timestamp = start_timestamp + 24 * 60 * 60 * 1000

    client = Elasticsearch(
        "http://elasticsearch:9200"
    )

    query = f"FROM emur_flow | WHERE datetime > {int(start_timestamp)} and datetime < {int(end_timestamp)} | LIMIT 1000"

    response = client.esql.query(
        query=query,
        format="csv",
    )
    df = pd.read_csv(StringIO(response.body))
    # convert the datetime column to a datetime object ignoring the hours
    df['datetime'] = pd.to_datetime(df['datetime'], unit='ms').dt.date
    grouped = df.groupby(['datetime', 'ProblemaPrincipale'], observed=False).size().reset_index(name='count')
    problems_count = {
        i: 0 for i in range(1, 32)
    }
    for date, problem, count in grouped.values:
        problems_count[int(problem)] += count
    problems = [0] * 31
    # convert the dictionary to a list
    for i in range(1, 32):
        problems[i - 1] = problems_count[i]
    return problems


def delete_predictions(date):
    """
    Delete the predictions for the given date.
    """
    print("Deleting predictions for date", date)
    client = Elasticsearch("http://elasticsearch:9200")

    # date is in a datetime.date format
    date = str(date)
    start_date = date + "T00:00:00"
    end_date = date + "T23:59:59"


    # Creazione della query per trovare i documenti con il campo datetime nel range specificato
    query = {
        "query": {
            "range": {
                "datetime": {
                    "gte": start_date,
                    "lte": end_date,
                    "format": "yyyy-MM-dd'T'HH:mm:ss"
                }
            }
        }
    }
    print("Query", query)

    # Esegui la cancellazione dei documenti che corrispondono alla query
    response = client.delete_by_query(index="emur_predictions", body=query)
    print("Response", response)
def notify_problems(problems, date):
    """
    Send the data to Elasticsearch. (to the emur_predictions index)
    """
    print("Notifying problems for date", date)
    client = Elasticsearch(
        "http://elasticsearch:9200"
    )
    for i in range(31):
        record = {
            "datetime": date,
            "ProblemaPrincipale": i + 1,
            "count": problems[i]
        }
        client.index(index="emur_predictions", body=record)

