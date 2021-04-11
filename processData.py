import pandas as pd

def processData():
    df = pd.read_pickle("./redditAPI_data.pkl")
    print(df)

if __name__ == "__main__":
    processData()