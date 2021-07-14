'''
Finnhub API docs
https://finnhub.io/docs/api/news-sentiment
'''

import requests
import numpy as np
import pandas as pd
import json
import os

# Get free finnhub key from here: https://finnhub.io/dashboard
finnhub_key = os.environ['FINNHUB_KEY']

def market_news(category='general'):
    '''
    Gets general market sentiment analysis
    category: str, can be one of general, crypto, forex, merger
    '''
    print('Getting market news...')
    r = requests.get(f'https://finnhub.io/api/v1/news?category={category}?&token={finnhub_key}')
    print(r.json())
    
    
def company_news_sentiment(symbol):
    '''
    Function to return company news senntiment from social media
    symbol: str, company ticker symbol (ex. AAPL)
    '''
    print(f'Getting sentiment analysis for {symbol}')
    r = requests.get(f'https://finnhub.io/api/v1/news-sentiment?symbol={symbol}&token={finnhub_key}')
    
#    May need to re-factor this dataframe
    df = pd.DataFrame.from_dict(r.json())
    print(df)
    
def get_company_news(symbol, start, end):
    '''
    returns all recent headlines centered on the company
    start, end: str, date interval of news request YYYY-MM-DD
    symbol: str, company ticker symbol (ex. AAPL)
    '''
    print('Fetching company news')
    r = requests.get(f'https://finnhub.io/api/v1/company-news?symbol=AAPL&from=2021-03-01&to=2021-03-09&token=c17ck1f48v6se55vrra0')
    
    print(r.json())
    
    
    


if __name__ == "__main__":
    company_news_sentiment('AMZN')
#    get_company_news('AAPL', '2021-01-04', '2021-07-13')
    market_news()


# TODO:
# Could make this^ one function - change out strings
# One API response function, call with diff request strings
# Add more Finnhub API features!


#def api_request(params):
#    res = requests(string + params + token)
#    print(res.json())
#
#    convert to df/numpy array



