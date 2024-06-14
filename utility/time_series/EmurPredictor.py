from collections import Counter
from datetime import timedelta

import pandas as pd
from river import linear_model, preprocessing, compose
from river import metrics
import datetime


class TimeSeriesPredictor:

    def __init__(self, df, target_col):
        """
        :param df: pandas DataFrame with time series data
        :param target_col: name of the target column to predict
        """
        # check if df has datetime column
        if 'datetime' not in df.columns:
            raise ValueError("df must have a datetime column")
        self.df = df
        self.target_col = target_col
        self.model = compose.Pipeline(
            preprocessing.StandardScaler(),
            linear_model.LinearRegression()
        )

    def fit(self):
        """
        Fit the model to the data in df
        """
        print("Fit the model")
        self.update(self.df)

    def update(self, new_df):
        """
        Update the model with new data
        :param new_df: pandas DataFrame with new data
        """
        for _, row in new_df.iterrows():
            x = row.drop(['datetime', self.target_col]).to_dict()
            y = row[self.target_col]
            self.model.learn_one(x, y)
        # add the new data to the original DataFrame
        self.df = pd.concat([self.df, new_df], ignore_index=True)

    def predict(self, k=1, simulations=100):
        """
        Predict the next k values of the target column
        :param k: number of target_col different values to predict
        :param simulations: number of simulations to perform
        :return: list of k predicted values
        """
        # Get the last date in the dataset
        last_date = self.df['datetime'].max().date()
        # Get the next date
        next_date = last_date + timedelta(days=1)
        # Create a DataFrame with the next date it has the same columns as the original DataFrame
        # and a placehoder row
        next_day_df = pd.DataFrame(columns=self.df.columns)
        next_day_df.loc[0] = {'datetime': next_date}

        # Predict the target column for the next date
        diagnoses_counter = Counter()

        # obtain a distribution of the target column values
        for _ in range(simulations):
            for _, row in next_day_df.iterrows():
                x = row.drop(['datetime']).to_dict()
                diagnosis = self.model.predict_one(x)
                diagnoses_counter[diagnosis] += 1

        # get the k most common diagnoses
        most_common_diagnoses = diagnoses_counter.most_common(k)

        return [diagnosis for diagnosis, _ in most_common_diagnoses]

    def next_datetime(self):
        """
        :return: the next datetime to predict
        """
        last_date = self.df['datetime'].max().date()
        return datetime.datetime.strptime(str(last_date + timedelta(days=1)), "%Y-%m-%d")


class EmurPredictor:

    def __init__(self, df, target_col):
        """
        :param df: pandas DataFrame with time series data
        :param target_col: name of the target column to predict
        """
        self.df = df
        self.target_col = target_col
        self.predictor = TimeSeriesPredictor(self.df, self.target_col)

    def fit(self):
        """
        Fit the model to the data in df
        """
        self.predictor.fit()

    def update(self, new_df):
        """
        Update the model with new data
        :param new_df: pandas DataFrame with new data
        """
        self.predictor.update(new_df)


    def predict(self, k=1):
        """
        :param k: number of target_col different values to predict
        :return: list of k predicted values
        """
        # Your code here
        return self.predictor.predict(k)

    def next_datetime(self):
        return self.predictor.next_datetime()
