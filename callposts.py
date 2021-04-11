import sys
import os
import time
import random
import requests
from datetime import datetime, date, timedelta
import pandas as pd

# A helpful resource: https://towardsdatascience.com/how-to-use-the-reddit-api-in-python-5e05ddfd1e5c

def makeURL(id):
    base_url = "https://www.reddit.com/r/wallstreetbets/comments/"
    base_url += str(id) + "/.json"
    return base_url

def is_validResponse(res):
    selftext = res.json()[0]['data']['children'][0]['data']['selftext']
    if (selftext == "[removed]"):
        return False
    if (selftext == ""):
        return False
    if (selftext == "[deleted]"):
        return False
    return True

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
            'id': post['data']['id']
        }, ignore_index=True)

    return df

# python callposts.py NUMBER_POSTS
# NUMBER_POSTS should be less than 100k (varies per subreddit and timerange)
# Guessing NUMBER_POSTS~1500-5000 would take 1 day
# For final dataset I would recommend 5000 and giving 1-3 days to run
def callposts():
    """
    # Proof of concept
    response = requests.get("https://www.reddit.com/r/wallstreetbets/comments/lglrg5/.json",headers={'User-agent': 'its_me/0.0.1'})
    print(response)
    print(response.json()[0]['data']['children'])
    #'created_utc', 'num_comments', 'id', 'banned_at_utc', 'removed_by', 'removal_reason', 'selftext', 'title', 'upvote_ratio', 'ups', 'likes', 
    return
    """

    total_posts = int(sys.argv[1])
    query_start = datetime(2021, 1, 12)
    query_end = datetime(2021, 2, 4)
    day2set = {}
    id_lists = []
    output_folder = "./dates.output/"
    for filename in os.listdir(output_folder):
        with open(output_folder + filename, "r") as var_output_file:
            lines = var_output_file.readlines()
            for line in lines:
                var_dt = datetime.fromtimestamp(int(line.split()[0]))
                if ((var_dt - query_start).days >= 0 and (var_dt - query_end).days <= 1):
                    var_day_diff = (var_dt - query_start).days
                    var_id = str(line.split()[1])
                    if (var_day_diff + 1 > len(id_lists)):
                        var_list = []
                        id_lists.append(var_list)
                    id_lists[var_day_diff].append(var_id)

                    if (var_day_diff in day2set):
                        var_set = day2set[var_day_diff]
                        var_set.add(var_id)
                        day2set[var_day_diff] = var_set
                    else:
                        var_set = set()
                        var_set.add(var_id)
                        day2set[var_day_diff] = var_set
    day2prop = {}
    total_len = 0
    for key in day2set:
        var_set = day2set[key]
        day2prop[key] = len(var_set)
        total_len += len(var_set)
    for key in day2prop:
        var_count = day2prop[key]
        day2prop[key] = float(var_count) / float(total_len)
    day2count = {}
    for key in day2prop:
        var_prop = day2prop[key]
        var_count = max(1, int(round(var_prop * total_posts)))
        day2count[key] = var_count

    data = pd.DataFrame()
    headers={'User-agent': 'its_me/0.0.1'}
    call_count = 0
    for key in day2count:
        counted = 0
        count_to = day2count[key]
        id_set = day2set[key]
        id_list = id_lists[key]
        while (counted < count_to):
            var_id = ""
            while(True):
                var_id = id_list[random.randrange(len(id_list))]
                if (var_id in id_set):
                    break
            var_url = makeURL(var_id)
            while(True):
                response = requests.get(var_url, headers=headers)
                if response.status_code == 200:
                    #Reddit API call limit: 60 calls per min
                    time.sleep(1)
                    break
                else:
                    print("bad request")
                    time.sleep(10)
            if (is_validResponse(response)):
                counted += 1
                call_count += 1
                if (call_count % 10 == 0):
                    print("Successful Call #:", call_count)
                    if (call_count % 10 == 0):
                        data.to_pickle("./redditAPI_data.pkl")
                new_df = df_from_response(response)
                data = data.append(new_df, ignore_index=True)
            id_set.remove(var_id)

    data.to_pickle("./redditAPI_data.pkl")
    return


if __name__ == "__main__":
    callposts()
