# Script to populate our training and testing databases with
# Financial company info: https://finnhub.io/docs/api/websocket-trades
# Finnhub page (log-in required):https://finnhub.io/dashboard

import pandas as pd
import numpy as np
import pandas_datareader as web
import matplotlib.pyplot as plt
import requests
import os
import json
import datetime as dt
import random

# Setup client
#finnhub_client = finnhub.Client(api_key="YOUR API KEY")
my_key = os.environ['FINNHUB_KEY']
r = requests.get(f'https://finnhub.io/api/v1/stock/symbol?exchange=US&token={my_key}')
#print(r.json(), type(r.json()))
company_list = r.json()

def get_company_data(company_symbol, start, end):
    '''
    Returns pandas dataframe of company
    '''
    print('Getting company data...')
    try:
        df = web.DataReader(company_symbol, 'yahoo', start, end)
        return df
    except web._utils.RemoteDataError:
        pass
    
    
if __name__ == "__main__":
    start = dt.datetime(2000, 1, 1)
    end = dt.datetime.now().date()
    training_path = os.path.join('.', 'data', 'training')
    testing_path = os.path.join('.', 'data', 'testing')
    valid_path = os.path.join('.', 'data', 'valid')
    n = 0
    for c in company_list[0:10]:
        print('Company raw data:', c)
        df = get_company_data(c['symbol'], start, end)
        print(df)
        if df is not None:
            weighted_choices = [(training_path, 4), (testing_path, 1)]
            population = [val for val, cnt in weighted_choices for i in range(cnt)]
            file_name = c['symbol'] + '-data.csv'
            path = os.path.join(random.choice(population), file_name)
            print('Path selected: ', path)
            df.to_csv(path)
            print('CSV saved!')
        print('Final DF:', df)
        print(n, '\n', '##########################')
        n += 1
        
