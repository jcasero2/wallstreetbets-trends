import sys
import requests

#python calldata.py LAST_X_POSTS
#Not sure why but LAST_X_POSTS must be less than 4
def calldata():
    count = sys.argv[1]
    base_url = "http://reddit.com/r/WallstreetBets/top/.json?count="
    call_url = base_url + str(count)
    response = requests.get(call_url)
    print(response.json())

if __name__ == "__main__":
    calldata()
