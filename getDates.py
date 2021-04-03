import time
import requests
from datetime import date, timedelta

def makeURL(query_date, duration):
    now = date.today()
    after = now - query_date
    after = after.days + 1
    before = after - duration
    base_url = "https://api.pushshift.io/reddit/search/submission/?subreddit=WallstreetBets"
    base_url += "&after=" + str(after) + "d&before=" + str(before) + "d&sort=asc&size=10"
    return base_url

def getDates():
    headers = {'User-agent': 'its me 0.0.1'}
    query_start = date(2021, 1, 12)
    query_end = date(2021, 2, 4)
    query_len = (query_end - query_start).days
    step_size = 1
    output_str = ""
    for i in range(int(query_len / step_size) + 1):
        query_date = query_start + timedelta(days=i)
        var_url = makeURL(query_date, step_size)
        response = {}
        while(True):
            response = requests.get(var_url, headers=headers)
            if response.status_code == 200:
                time.sleep(2)
                break
            else:
                time.sleep(10)
        for post in response.json()["data"]:
            output_str += str(post["created_utc"]) + "\t" + str(post["id"]) + "\n"
    with open("dates.output", "w") as output:
        output.write(output_str)
    return


if __name__ == "__main__":
    getDates()
