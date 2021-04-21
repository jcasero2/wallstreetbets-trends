# wallstreetbets-trends
Using Sentiment Analysis from r/WallStreetBets to Predict Stock Perfomance


## Motivation
Investor opinion and market sentiment have long been used to augment technical analysis for stocks. Through r/WallStreetBets schemed short-squeeze of Game- Stock, AMC, Nokia, and others, the market saw drastic impact from this subreddit. We aim to investigate if r/WallstreetBets is a legitimate soucre to base investments upon. 


## Install
1. Create virtual environment and activate:
```python3 -m venv env```
```source env/bin/activate```

2. Install requirements:
```pip3 install -r requirements.txt```


## API Refrence
Reddit API: https://www.reddit.com/dev/api/
Pushshift Reddit Search API: https://github.com/pushshift/api


## Usage
The program runs on user input: a date range and number of top stocks displayed. On running
```python3 main.py```
A user will enter their desiered date range and a number N (stocks to display), and the program will pull data necessary to extract all posts from r/WallStreetBets for the given time period. It will then examine each post and classify it to a stock in the NYSE, if any. Once identified, a sentiment score will be calculated on the post and a final score will be given, which takes the post's popularity and rating on r/WallStreetBets into account. Meanwhile, an index is being built as each post is examined, and when the entirty of the posts have been inspected, the index will indicate the highest N rated stocks in the index as either a LONG (positive score) or SHORT (negative score) position.

If the date range entered is in the past, the program will run an analysis on historical stock data using yahoo finance to determine the trend prediction accuracy for the stocks returned and the Kendall-Tau Distance to optimal ranking for the ordering of the list when compared to the historical data.

The following list explains how each component of the program works.

### generateStockList.py
Uses the nyse_stocks.py to build tickers.pickle - a comprehensive DataFrame of all NYSE stock tickers and the names of the companies they represent.

### getDates.py
Calls the Pushshift Reddit Search API for a specified date to pull all posts from r/WallStreetBets on that day and outputs this list of unix timestamps withccorrelating post ID's as a new file in the dates/ directory.

### callposts.py
Finds the list of post ID's created by getDates for a specified day and calls the Reddit API for each post to create a Dataframe of:

Post Title
Post Text
Upvote Ratio
Total Upvotes
Total Downvotes
Post ID

for all posts on r/WallStreetBets for the specified day. It ouputs the serialized DataFrame as a new file in the posts/ directory.

### processData.py
Deserializes the DataFrame created by callposts for a specific day and calculates a sentiment score for each post on that day. It outputs an index for the given day which maps all stock tickers mentioned on r/WallStreetBets to their respective scores calculated as follows:

score at stock ticker X = sum for all posts mentioning X ( sentiment score of post * log(total votes on post) * upvote ratio of post )

This index is combined with others created over the user's date range to run the prediction analysis in main.py.

