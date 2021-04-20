from callposts import callposts
from getDates import getDates
from processData import processData
import os
import datetime
import string
import pickle

def convert_date_to_tuple(string):
    temp = string.split("-")
    return (int(temp[0]), int(temp[1]), int(temp[2]))
x = input("Input start date (YYYY-MM-DD): ")
y = input("Input end date (YYYY-MM-DD): ")
n = input("Input size of ranked list: ")

(s_year, s_month, s_day) = convert_date_to_tuple(x)
(e_year, e_month, e_day) = convert_date_to_tuple(y)

epoch_start = datetime.date(s_year, s_month, s_day)
epoch_end = datetime.date(e_year, e_month, e_day)
delta =  epoch_end - epoch_start

date_list = []
for i in range(delta.days + 1):
    day = epoch_start + datetime.timedelta(days = i)
    date_list.append(convert_date_to_tuple(day.strftime('%Y-%m-%d')))

#check if corresponding dataframes exist
positive_words = set()
negative_words = set()
with open("positive_words.txt") as pos_words:
    for word in pos_words.readlines():
        positive_words.add(word.rstrip())

with open("negative_words.txt") as neg_words:
    for word in neg_words.readlines():
        negative_words.add(word.rstrip())

with open("tickers.pickle", "rb") as tickers:
    stock_map = pickle.load(tickers)

s_scores = []
for tuple in date_list:
    path = "posts/"
    filename = "Posts-" + str(tuple[1]) + "-" + str(tuple[2]) + "-" + str(tuple[0]) + ".pickle"
    dataFrame_name = os.path.join(path, filename)
    if not os.path.exists(dataFrame_name):
        print("Does not exist --> generating list of postID's")
        getDates(str(tuple[1]), str(tuple[2]), str(tuple[0]))
        print("Finished postID list --> generating dataFrame")
        callposts(str(tuple[1]), str(tuple[2]), str(tuple[0]),10)
    s_scores.append(processData(str(tuple[1]), str(tuple[2]), str(tuple[0]),
                                 positive_words, negative_words, stock_map))

sentiment_index = {}
#combine all score_index
for index in s_scores:
    for k,v in index.items():
        if k not in sentiment_index:
            sentiment_index[k] = 0
        sentiment_index[k] += v

sorted_stock_scores = sorted(sentiment_index.items(), key = lambda x: abs(x[1]), reverse=True)

list_size = min(int(n), len(sorted_stock_scores))
print(sorted_stock_scores[:list_size])