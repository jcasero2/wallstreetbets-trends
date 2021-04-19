import sys
import os
import time
import random
import requests
import datetime
import pandas as pd

response = requests.get("https://www.reddit.com/r/wallstreetbets/comments/mhn63v/.json",headers={'User-agent': 'its_me/0.0.1'})
print(response.status_code)