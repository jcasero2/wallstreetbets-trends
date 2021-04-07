import sys
import time
import requests
from datetime import datetime, date, timedelta
import pandas as pd

# A helpful resource: https://towardsdatascience.com/how-to-use-the-reddit-api-in-python-5e05ddfd1e5c

def makeURL(id):
    base_url = "https://www.reddit.com/r/wallstreetbets/comments/"
    base_url += str(id) + "/.json"
    return base_url

def df_from_response(res):
    # initialize temp dataframe for batch of data in response
    df = pd.DataFrame()

    # loop through each post pulled from res and append to df
    for post in res.json()[0]['data']['children']:
        df = df.append({
            'title': post['data']['title'],
            'selftext': post['data']['selftext'],
            'upvote_ratio': post['data']['upvote_ratio'],
            'ups': post['data']['ups'],
            'downs': post['data']['downs'],
            'num_commnets': post['data']['num_comments'],
            'banned_at_utc': post['data']['banned_at_utc'],
            'removed_by': post['data']['removed_by'],
            'removal_reason': post['data']['removal_reason'],
            'created_utc': datetime.fromtimestamp(post['data']['created_utc']).strftime('%Y-%m-%dT%H:%M:%SZ'),
            'id': post['data']['id'],
            'likes': post['likes']
        }, ignore_index=True)

    return df

def callposts():
    """
    # Proof of concept
    response = requests.get("https://www.reddit.com/r/wallstreetbets/comments/lglrg5/.json",headers={'User-agent': 'its_me/0.0.1'})
    print(response)
    print(response.json()[0]['data']['children'])
    #'created_utc', 'num_comments', 'id', 'banned_at_utc', 'removed_by', 'removal_reason', 'selftext', 'title', 'upvote_ratio', 'ups', 'likes', 
    return
    """

    data = pd.DataFrame()
    headers={'User-agent': 'its_me/0.0.1'}
    call_count = 0
    with open("dates.output", "r") as dates:
        lines = dates.read_lines()
        for line in lines:
            var_timestamp = line.split()[0]
            var_id = line.split()[1]
            var_url = makeURL(var_id)
            while(True):
                response = requests.get(var_url, headers=headers)
                if response.status_code == 200:
                    #Reddit API call limit: 60 calls per min
                    time.sleep(1)
                    call_count += 1
                    if (call_count % 100 == 0):
                        print("call #:", call_count)
                        if (call_count % 1000 == 0):
                            data.to_pickle("./redditAPI_data.pkl")
                    break
                else:
                    print("bad request")
                    time.sleep(10)
            new_df = df_from_response(response)
            data = data.append(new_df, ignore_index=True)

    data.to_pickle("./redditAPI_data.pkl")
    return


if __name__ == "__main__":
    callposts()
