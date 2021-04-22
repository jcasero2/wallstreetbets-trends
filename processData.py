import pandas as pd
""" 
pip install wheel
pip install pandas
"""
import pickle
import re
import string 
from preprocess import pprocess
import os
import math


"""
processData:
the file at respective month/day/year is processed and an index of 
all tickers -> sentiment score is returned for the given day.
"""
def processData(month, day, year, positive_words, negative_words, stock_map):
    # file to process
    path = "posts/"
    filename = "Posts-" + month + "-" + day + "-" + year + ".pickle"
    dataFrame_name = os.path.join(path, filename)

    df = pd.read_pickle(dataFrame_name)
    title_list = df.title.astype(str)
    ups_list = df.ups.astype(str)
    downs_list = df.downs.astype(str)
    ratio_list = df.upvote_ratio.astype(str)
    text_list = df.selftext.astype(str)

    # create scoring and traverse data
    stock_scores = {}
    for i, title in enumerate(title_list):
        title = title.split()
        for word in title:
            clean = re.sub('[$]', '', word)
            if clean in stock_map:
                if clean not in stock_scores:
                    stock_scores[clean] = 0
                score = math.log10(float(ups_list[i]) + float(downs_list[i]) + 2)
                score *= float(ratio_list[i])
                score *= float(calculate_sentiment(title, text_list[i], positive_words, negative_words))
                stock_scores[clean] += score

    return stock_scores

def calculate_sentiment(title, text, positive_words, negative_words):
    score = 0
    for word in title:
        word = word.lower()
        if word in positive_words: score += 1
        elif word in negative_words: score -= 1
    for word in text.split():
        word = word.lower()
        if word in positive_words: score += 1
        elif word in negative_words: score -= 1
    return score > 0 and 2 or -2
    
