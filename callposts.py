import sys
import os
import time
import random
import requests
import datetime
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
            # 'num_commnets': post['data']['num_comments'],
            # 'banned_at_utc': post['data']['banned_at_utc'],
            # 'removed_by': post['data']['removed_by'],
            # 'removal_reason': post['data']['removal_reason'],
            # 'created_utc': datetime.fromtimestamp(post['data']['created_utc']).strftime('%Y-%m-%dT%H:%M:%SZ'),
            'id': post['data']['id']
        }, ignore_index=True)

    return df

# python callposts.py NUMBER_POSTS
# NUMBER_POSTS should be less than 100k (varies per subreddit and timerange)
# Guessing NUMBER_POSTS~1500-5000 would take 1 day
# For final dataset I would recommend 5000 and giving 1-3 days to run
def callposts(month, day, year, max_posts):
    """
    # Proof of concept
    response = requests.get("https://www.reddit.com/r/wallstreetbets/comments/lglrg5/.json",headers={'User-agent': 'its_me/0.0.1'})
    print(response)
    print(response.json()[0]['data']['children'])
    #'created_utc', 'num_comments', 'id', 'banned_at_utc', 'removed_by', 'removal_reason', 'selftext', 'title', 'upvote_ratio', 'ups', 'likes', 
    return
    """
    query_start = datetime.datetime(int(year), int(month), int(day), 0, 0).strftime('%s')
    query_end= datetime.datetime(int(year), int(month), int(day), 23, 59).strftime('%s')
    id_list = []
    filename = "dates.output-" + str(month) + "-" + str(day) + "-" + str(year)
    path = "dates/"
    with open(os.path.join(path, filename), "r") as var_output_file:
        lines = var_output_file.readlines()
        for line in lines:
            post_id = str(line.split()[1])
            id_list.append(post_id)
    
    data = pd.DataFrame()
    headers={'User-agent': 'its_me/0.0.1'}
    call_count = 0
    counted = 0
    for id in id_list:
        if(counted >= max_posts and max_posts != 0):
            break
        var_url = makeURL(id)

        while(True):
                response = requests.get(var_url, headers=headers)
                #response = requests.get("https://www.reddit.com/r/wallstreetbets/comments/mhn63v/.json",headers={'User-agent': 'its_me/0.0.1'})
                # print(response)
                if response.status_code == 200:
                    #Reddit API call limit: 60 calls per min
                    # print("success")
                    time.sleep(1)
                    break
                else:
                    print("bad request")
                    time.sleep(1.5)

        if (is_validResponse(response)):
                counted += 1
                call_count += 1
                new_df = df_from_response(response)
                data = data.append(new_df, ignore_index=True)

    output_path = "posts/"
    if not os.path.exists(output_path):
        os.makedirs(output_path)
    output_filename = "Posts-" + str(month) + "-" + str(day) + "-" + str(year) + ".pickle"
    output = os.path.join(output_path, output_filename)
    data.to_pickle(output)
    return

if __name__ == "__main__":
    callposts(3,31,2021,50)
