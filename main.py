from callposts import callposts
from getDates import getDates
from processData import processData
import os
import datetime
import string
import pickle
import yfinance as yf
from scipy import stats
from tabulate import tabulate
from pandas_datareader import data as pdr
import pandas as pd

def calculate_next_week_day(day):    
    if day.isoweekday()== 5:
        day += datetime.timedelta(days=3)
    elif day.isoweekday()== 6:
        day += datetime.timedelta(days=2)
    else:
        day += datetime.timedelta(days=1)
    return day

def price_for_date(year ,month ,day ,stock_ticker):

    start_date = ""
    end_date = ""
    start_date = str(year) + "-" + str(month) + "-" + str(day)
    end_date = str(year) + "-" + str(month) + "-" + str(int(day) + 1)

    data = pdr.get_data_yahoo(stock_ticker, start= start_date , end= end_date)

    return data['Adj Close'].iloc[0]

def calculate_kendall(ranking1 , ranking2 ):

    tau, p_value = stats.kendalltau( ranking1, ranking2)

    return tau

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
final_list = sorted_stock_scores[:list_size]

f_list = []
for i in range(list_size):
    temp_arr = []
    pair = sorted_stock_scores[i]
    temp_arr.append(stock_map[pair[0]])
    if float(pair[1]) > 0:
        temp_arr.append("Long")
    else:
        temp_arr.append("Short")
    f_list.append(temp_arr)
print(tabulate(f_list, headers=['Stock', 'Long/Short Position']))
#####Evaluation###### Only uncomment when running on a historical date range and on ranges that dont include holidays
print("\n")
correct = 0
count = 0
change_list = []
f_list = []
for pair in final_list:
    temp_arr = []
    count +=1
    temp_arr.append(stock_map[pair[0]])
    if float(pair[1]) > 0:
        temp_arr.append("Long")
    else:
        temp_arr.append("Short")

    next_day = calculate_next_week_day(epoch_end)
    (n_year, n_month, n_day) = convert_date_to_tuple(next_day.strftime('%Y-%m-%d'))
    #print(str(n_year) + " " + str(n_month) + str(n_day))
    new_p = price_for_date(n_year, n_month, n_day, pair[0])
    old_p = price_for_date(e_year, e_month, e_day, pair[0])
    change =  round(((new_p - old_p)/ old_p) * 100, 2)
    change_list.append(change)
    temp_arr.append(str(change))
    f_list.append(temp_arr)
    if (float(pair[1]) * float(change)) > 0: #both the change and the predicted change are of the same sign
        correct += 1
print(tabulate(f_list, headers=['Stock', 'Long/Short Position', 'Price Change %']))
accuracy = float(correct)/count * 100
print("Trend Prediction Accuracy = " + str(accuracy) + "%")

our_ranking = list(range(1,(int(n)+1)))
our_ranking.reverse() # we reverse the list as the value of the first stock we think will be the highest
change_list = [abs(number) for number in change_list]
print("Kendall-Tau Distance to optimal ranking: " + str(calculate_kendall(our_ranking, change_list)))