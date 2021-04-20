import time
import requests
import datetime
import os

def getDates(month, day, year):
    headers = {'User-agent': 'bot4school/0.0.1'}
    params = {'subreddit': 'WallstreetBets', 'after': '', 'size': 500, 'sort': 'asc', 'author_removed': False,
    'mod_removed': False, 'author': '![deleted]'}

    query_start_unix = datetime.datetime(int(year), int(month), int(day), 0, 0).strftime('%s')
    query_end_unix= datetime.datetime(int(year), int(month), int(day), 23, 59).strftime('%s')

    path = "dates/"
    if not os.path.exists(path):
        os.makedirs(path)
    output_str = ""
    output_filename = "dates.output-" + str(month) + "-" + str(day) + "-" + str(year)

    params['after'] = str(int(query_start_unix))
    count = 0
    while (int(params['after']) < int(query_end_unix)):
        while(True):
            response = requests.get("https://api.pushshift.io/reddit/search/submission/", headers=headers, params=params)
            if response.status_code == 200:
                #Pushshift API call limit: 200 calls per min
                time.sleep(60/200)
                break
            else:
                print("bad request")
                #time.sleep(10) WHY 10 Seconds
                time.sleep(1)

        data = response.json()["data"]
        for post in data:
            if int(post["created_utc"]) > int(query_end_unix):
                break
            output_str += str(post["created_utc"]) + "\t" + str(post["id"]) + "\n"
            count += 1
        params['after'] = str(int(data[len(data) - 1]['created_utc']))
        if count > 1000: break

    with open(os.path.join(path, output_filename), "w") as output:
        output.write(output_str)
    return

if __name__ == "__main__":
    getDates(4,5,2021)
