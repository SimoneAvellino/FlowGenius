import pandas as pd

csv_files = ['data/2021.csv', 'data/2022.csv', 'data/2023.csv']

df = pd.concat([pd.read_csv(file) for file in csv_files])

# keep only date and problema_principale columns
df = df[['data', 'problema_principale']]

# don't consider hours, minutes and seconds
df['data'] = pd.to_datetime(df['data']).dt.date

# group by date and problema_principale
grouped = df.groupby(['data', 'problema_principale'], observed=False).size().reset_index(name='count')

# pivot the dataframe
pivot_df = grouped.pivot(index='data', columns='problema_principale', values='count')

# fill NaN values with 0
pivot_df = pivot_df.fillna(0)

# reset index
pivot_df = pivot_df.reset_index()

# rename columns
pivot_df.columns.name = None

# sort by date
pivot_df = pivot_df.sort_values(by='data')

# save to csv
pivot_df.to_csv('data/time_series.csv', index=False)