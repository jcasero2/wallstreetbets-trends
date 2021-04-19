import pandas as pd
""" 
pip install wheel
pip install pandas
"""
import pickle
import re
import string 
from preprocess import pprocess


"""
data available:

banned_at_utc
created_utc
downs
id
num_commnets
removal_reason
removed_by
selftext
title
ups
upvote_ratio

positive_words and negative_words are sets used for sentiment analysis
stock_map dict of all company's ticker -> company's name

processData:
the file at respective month/day/year is processed and an index of 
all tickers -> sentiment score is returned for the given day.
"""
def processData(month, day, year, positive_words, negative_words, stock_map):
    # file to process
    filename = f'./posts-{month}-{day}-{year}.pkl'
    df = pd.read_pickle(filename)
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
                score = float(ups_list[i]) + float(downs_list[i])
                score *= float(ratio_list[i])
                score *= float(calculate_sentiment(title, text_list[i], positive_words, negative_words))
                stock_scores[clean] += score

    # for x in range(size):
    #     t = df["title"].iloc[x]
    #     t_list = pprocess(t)
    #     for word in t_list:
    #         clean = re.sub('[$]', '', word)
    #         if clean in stock_map:
    #             if clean not in stock_count:
    #                 stock_count[clean] = 0
    #             stock_count[clean] += 1
    sorted_stock_scores = sorted(stock_scores.items(), key = lambda x: abs(x[1]), reverse=True)
    print(sorted_stock_scores)
    return sorted_stock_scores
    # total_stock_references = 0
    # for pair in sorted_stock_scores:
    #     print(stock_map[pair[0]] + ": " + str(pair[1]))
    #     total_stock_references += pair[1]
    # print("Total Number of stocks mentioned: " + str(total_stock_references))


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
    # return sentiment score
    # print(f' The score is : {score}')
    return score > 0 and 2 or -2



if __name__ == "__main__":
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
    
    processData(1,1,1,positive_words,negative_words,stock_map)
    