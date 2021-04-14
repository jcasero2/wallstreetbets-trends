import pandas as pd
import pickle
csv_file = "./nyse_stocks.csv"
df = pd.read_csv(csv_file)
df = df.filter(['Symbol', 'Name'])
df['Symbol'] = df.Symbol.astype(str)
df['Name'] = df.Name.astype(str)
ticker_to_name = {}
for index, row in df.iterrows():
    ticker_to_name[row['Symbol']] = row['Name']
# print(df['Name'].iloc[0])
# print(ticker_to_name['GME'])
file_to_write = open("tickers.pickle", "wb")
pickle.dump(ticker_to_name, file_to_write)