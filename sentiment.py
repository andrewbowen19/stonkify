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

def general_news_sentiment():
    '''
    Gets general market sentiment analysis
    '''
    print('Getting market news...')
    
    
def company_news_sentiment(symbol):
    '''
    Function to return company news senntiment from social media
    '''
    print(f'Getting sentiment analysis for {symbol}')
    r = requests.get(f'https://finnhub.io/api/v1/news-sentiment?symbol=DIS&token={finnhub_key}')
    
#    May need to re-factor this dataframe
    df = pd.DataFrame.from_dict(r.json())
    print(df)

if __name__ == "__main__":
    company_news_sentiment('AMZN')
