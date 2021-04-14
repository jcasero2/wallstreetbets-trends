import pandas as pd
import pickle
import re
import string 
from preprocess import pprocess

def processData():
    with open("tickers.pickle", "rb") as tickers:
        stock_map = pickle.load(tickers)
    df = pd.read_pickle("./redditAPI_data_100.pkl")
    df['title'] = df.title.astype(str)
    stock_count = {}
    size = len(df.index)
    for x in range(size):
        t = df["title"].iloc[x]
        t_list = pprocess(t)
        for word in t_list:
            clean = re.sub('[$]', '', word)
            if clean in stock_map:
                if clean not in stock_count:
                    stock_count[clean] = 0
                stock_count[clean] += 1
    sorted_stock_count = sorted(stock_count.items(), key = lambda x: x[1], reverse=True)
    total_stock_references = 0
    for pair in sorted_stock_count:
        print(stock_map[pair[0]] + ": " + str(pair[1]))
        total_stock_references += pair[1]
    print("Total Number of stocks mentioned: " + str(total_stock_references))


if __name__ == "__main__":
    processData()