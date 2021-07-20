# Stock data visualization dashboard
# Awesome-quent list of packages for fin data: https://github.com/wilsonfreitas/awesome-quant#data-sources

import os
import pandas as pd
import matplotlib.pyplot as plt
import pandas_datareader as web
import finnhub
from dateutil import parser
import datetime as dt

# Dash imports
import plotly.express as px
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import dash_table
# import sklearn
from scipy import optimize

from sentiment import finnhub_api_request

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server # server needed for heroku deploy

# Get free finnhub key from here: https://finnhub.io/dashboard
finnhub_key = os.environ['FINNHUB_KEY']
finnhub_client = finnhub.Client(api_key=finnhub_key)

def test_func(x, dist, amp, omega, phi):
    # For a sinusoidal model: https://towardsdatascience.com/fitting-cosine-sine-functions-with-machine-learning-in-python-610605d9b057
    return dist + amp * np.cos(omega * x + phi)

def convert_to_unix(date_str):
    '''
    Converts a ISO 8601 datetime string to a UNIX timestamp (number)
    date: datetime obj
    
    returns; unix timestamp in integer forma
    '''
    unix = int(parser.parse(date_str).timestamp())

    return unix



print('Getting stock data...')
default_symbol = 'AAPL'

# UNIX timestamps of default start/end dates
default_start = dt.datetime(2020, 1, 1)
default_end = dt.datetime.now().date().strftime('%Y-%m-%d ')
start_me = int(parser.parse('2020-01-01').timestamp())
end_me = int(parser.parse(default_end).timestamp())

# Default dataframe

ddf = pd.DataFrame(finnhub_client.stock_candles('AAPL', 'D', start_me, end_me))
print('FOO', ddf)
ddf['t'] = [dt.datetime.fromtimestamp(t).strftime('%Y-%m-%d') for t in ddf['t']]
#Resetting DF columns
new_cols = ['Close', 'High', 'Low', 'Open', 'Status', 'Date', 'Volume']
ddf.columns = new_cols

ddf = ddf.drop(['Status'], axis=1)

print('Default Stock data:\n', ddf)
f = px.line(ddf, x=ddf.index, y='Close', title=default_symbol)


#############################################
# Creating app layout
app.layout = html.Div(children=[

    html.H1('Welcome to Stonk World.', style={'text-align':'center'}),

    # Search field -- user input
    html.Div(className='row', children=[
            # Symbol lookup
            html.Div([
                    dcc.Input(
                    id='lookup-stock',
                    type='text',
                    placeholder="Search Stock Symbol",
                    value='AAPL',
                    debounce=True
                    )
                    ], className='two columns'),

            # Data desired (price, open, close, etc.)
            html.Div([
                    dcc.Dropdown(
                        id='price-selection',
                        options=[{'label': x, 'value': x} for x in ddf.columns],
                        value='Close'
                        )
                    ], className='two columns'),

            # Start & end date selection
            html.Div([

                    dcc.DatePickerRange(
                        id='date-selector',
                        min_date_allowed=dt.date(1985,1,1),
                        max_date_allowed=dt.datetime.now().date(),
                        start_date=dt.datetime(2020,1,1),
                        end_date=dt.datetime.now().date()
                        )

                    ])
            
            ]),

    # Stock graph - main view of dashboard
    html.Div([
            dcc.Graph(
            id='stock-graph',
            figure=f
            )
            ]),

    # User can select model
    html.Div([
            dcc.Checklist(
                id='model-selector',
                options=[{'label': 'Show trend model?', 'value': 'True'}],
                value=[],
                labelStyle={'display': 'inline-block'}
                )

            ], className='two columns'),
   
#   Table with ind stock data
   html.Div([
            dash_table.DataTable(
            id='stock-table',
            columns=[{"name": i, "id": i} for i in ddf.columns],
#            data=df.to_dict('records')
            )
            ])
])

# Updating graph based on user input values
@app.callback(
    Output('stock-graph', 'figure'),
    Output('stock-table', 'data'),
    [Input('lookup-stock', 'value'),
     Input('price-selection', 'value'),
     Input('date-selector', 'start_date'),
     Input('date-selector', 'end_date'),
     Input('model-selector', 'value')]
    )
def update_stock_data(value, price, start_date, end_date, model):
    '''
    Lookup new stock prices with user input
    Updates both stock graph AND data table below based on user input
    Value: str, inputted ticker symbol
    start_date, end_date: datetime object, needs to be converted to UNIX timestamp. Start and end-periods of price lookup
    '''
    #    df = web.DataReader(value, 'yahoo', start_date, end_date)

    start = convert_to_unix(start_date)
    
    end = convert_to_unix(end_date)
    df = pd.DataFrame(finnhub_client.stock_candles(value,'D', start, end))
    
#    Converting timestamp for readability and changing column names
    df['t'] = [dt.datetime.fromtimestamp(t).strftime('%Y-%m-%d') for t in df['t']]
    df.drop(['s'], axis=1)
    df.columns = new_cols

    print(f'New stock searched: {value}')
    print(df.head())

    # Creating figure
    f = px.line(df, x=df.index, y=price, title=value)

    if model=='True':
        print('Generating model...')

    return [f, df[['Close', 'High', 'Low', 'Open','Date', 'Volume']].head(n=10).to_dict('records')]

# Run the app
if __name__ == "__main__":
    print(dt.datetime.fromtimestamp(15705789).strftime('%Y-%m-%d %H:%M:%S'))
    app.run_server(debug=True)
    

# TODO:

#    -Add symbol lookup (Check Finnhub's function: https://finnhub.io/docs/api/symbol-search)
#    -Clean up



