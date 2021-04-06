import sys
import time
import requests
from datetime import datetime, date, timedelta
import pandas as pd

# A helpful resource: https://towardsdatascience.com/how-to-use-the-reddit-api-in-python-5e05ddfd1e5c

def dateRange(q_start, q_end):
    dates_dict = {}
    with open("dates.output", "r") as dates:
        lines = dates.readlines()
        for line in lines:
            var_dt = datetime.fromtimestamp(int(line.split()[0]))
            var_id = "t3_" + str(line.split()[1])
            dates_dict[var_id] = var_dt
        return dates_dict

def get_end_id(end_date, dates):
    min_record = date(2222, 2, 2)
    min = 100000000000000
    for id in dates:
        var_date = dates[id]
        if (end_date < var_date):
            var_seconds = (var_date - end_date).total_seconds()
            if (var_seconds < min):
                min = var_seconds
                min_record = var_date
    return min_record

def get_start_id(start_date, dates):
    min_record = date(2222, 2, 2)
    min = 100000000000000
    for id in dates:
        var_date = dates[id]
        if (start_date > var_date):
            var_seconds = (start_date - var_date).total_seconds()
            if (var_seconds < min):
                min = var_seconds
                min_record = var_date
    return min_record

def df_from_response(res):
    # initialize temp dataframe for batch of data in response
    df = pd.DataFrame()

    # loop through each post pulled from res and append to df
    for post in res.json()['data']['children']:
        df = df.append({
            'subreddit': post['data']['subreddit'],
            'title': post['data']['title'],
            'selftext': post['data']['selftext'],
            'upvote_ratio': post['data']['upvote_ratio'],
            'ups': post['data']['ups'],
            'downs': post['data']['downs'],
            'score': post['data']['score'],
            'link_flair_css_class': post['data']['link_flair_css_class'],
            'created_utc': datetime.fromtimestamp(post['data']['created_utc']).strftime('%Y-%m-%dT%H:%M:%SZ'),
            'id': post['data']['id'],
            'kind': post['kind']
        }, ignore_index=True)

    return df

#python calldata.py REDDIT_USERNAME REDDIT_PASSWORD
#Note: Any username and password will not work.  You must be added as a 
#      developeron the project by Abe Schon (schonabr@umich.edu, 517-525-4159) 
#      and then utilize your reddit login credentials.
def calldata():
    username = sys.argv[1]
    password = sys.argv[2]
    # authenticate API
    client_auth = requests.auth.HTTPBasicAuth('IA-Egc7sqZey-A', 'Ti6sX2LZH-j4Y7VOT_ZrgublmZGFVA')
    data = {
        'grant_type': 'password',
        'username': username,
        'password': password
    }
    headers = {'User-Agent': 'EECS486GroupProject/0.0.1'}

    # send authentication request for OAuth token
    res = requests.post('https://www.reddit.com/api/v1/access_token',
                        auth=client_auth, data=data, headers=headers)
    print(res.json())
    # extract token from response and format correctly
    token = f"bearer {res.json()['access_token']}"
    # update API headers with authorization (bearer token)
    headers = {**headers, **{'Authorization': token}}

    # initialize dataframe and parameters for pulling data in loop
    data = pd.DataFrame()
    params = {'limit': 100}
    base_url = "https://oauth.reddit.com/r/WallstreetBets/new"

    query_start = datetime(2021, 1, 12)
    query_end = datetime(2021, 2, 4)
    dates = dateRange(query_start, query_end)
    start_id = get_start_id(query_start, dates)
    end_id = get_end_id(query_end, dates)
    params['after'] = end_id
    params['count'] = 0
    call_count = 0
    while(start_id not in data.values):
        while(True):
            res = requests.get(base_url,
                        headers=headers,
                        params=params)
            call_count += 1
            if res.status_code == 200:
                time.sleep(2)
                break
            else:
                print("bad request")
                time.sleep(10)
        # get dataframe from response
        new_df = df_from_response(res)
        # take the final row (oldest entry)
        if (new_df.shape[0] > 0):
            params['count'] = params['count'] + new_df.shape[0]
            row = new_df.iloc[len(new_df)-1]
            # create fullname
            fullname = row['kind'] + '_' + row['id']
            # add/update fullname in params
            params['after'] = fullname
            
            # append new_df to data
            data = data.append(new_df, ignore_index=True)
        else:
            print(call_count)
            break

    data.to_pickle("./redditAPI_data.pkl")
    print(data)
    return

    """
    base_url = "http://reddit.com/r/WallstreetBets/new/"
    call_url = base_url + str(count)
    response = requests.get(call_url, headers=headers, params=params)
    print(response.json())
    """


if __name__ == "__main__":
    calldata()
