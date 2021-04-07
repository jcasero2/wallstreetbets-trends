import time
import requests
from datetime import datetime, date, timedelta

def getDates():
    headers = {'User-agent': 'bot4school/0.0.1'}
    params = {'subreddit': 'WallstreetBets', 'after': '1611944804', 'size': 500, 'sort': 'asc'}
    query_start = date(2021, 1, 11)
    query_start_unix = time.mktime(query_start.timetuple())
    #params['after'] = str(int(query_start_unix))
    query_end = date(2021, 2, 5)
    query_end_unix = time.mktime(query_end.timetuple())
    output_str = ""
    call_count = 0
    file_count = 6
    output_filename = "dates.output" + str(file_count)
    while (int(params['after']) < int(query_end_unix)):
        while(True):
            response = requests.get("https://api.pushshift.io/reddit/search/submission/", headers=headers, params=params)
            if response.status_code == 200:
                #Pushshift API call limit: 200 calls per min
                time.sleep(60/200)
                call_count += 1
                if (call_count % 50 == 0):
                    print("call #:", call_count)
                    print("datapoints:", call_count * 100)
                    if (call_count % 1000 == 0):
                        file_count += 1
                        output_filename = "dates.output" + str(file_count)
                        output_str = ""
                        time.sleep(60)
                    with open(output_filename, "w") as output:
                        output.write(output_str)
                break
            else:
                print("bad request")
                time.sleep(10)
        data = response.json()["data"]
        for post in data:
            output_str += str(post["created_utc"]) + "\t" + str(post["id"]) + "\n"
        params['after'] = str(int(data[len(data) - 1]['created_utc']))
    with open(output_filename, "w") as output:
        output.write(output_str)
    return


if __name__ == "__main__":
    getDates()
