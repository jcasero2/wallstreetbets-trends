import sys
import requests

# A helpful resource: https://towardsdatascience.com/how-to-use-the-reddit-api-in-python-5e05ddfd1e5c

#python calldata.py LAST_X_POSTS
#Not sure why but LAST_X_POSTS must be less than 4
def calldata():
    count = sys.argv[1]
    params = {'after': "t3_mj5rgl"}
    headers = {'User-agent': 'its me 0.0.1'}
    base_url = "http://reddit.com/r/WallstreetBets/top/.json?count="
    call_url = base_url + str(count)
    response = requests.get(call_url, headers=headers, params=params)
    print(response.json())


if __name__ == "__main__":
    calldata()
