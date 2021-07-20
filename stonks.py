# Stock data visualization dashboard
# Awesome-quent list of packages for fin data: https://github.com/wilsonfreitas/awesome-quant#data-sources

import os
import pandas as pd
import matplotlib.pyplot as plt
import pandas_datareader as web
import finnhub
from datetime import timezone
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

print('Getting stock data...')
default_symbol = 'AAPL'

# These need to be unix timestamps
start = dt.datetime(2000, 1, 1)
end = dt.datetime.now().date()


res = finnhub_client.stock_candles('AAPL', 'D', 1590988249, 1591852249)

ddf = pd.DataFrame(res)
new_cols = ['Close', 'High', 'Low', 'Open', 'Status', 'Timestamp', 'Volume']
ddf.columns = new_cols


# May need to use different API thatn pandas datareader - switch to finnhub API
# Will also need to convert Finnhub API response to DF
#ddf = web.DataReader(default_symbol, 'yahoo', start, end)




print(ddf)#.head())
f = px.line(ddf, x=ddf.index, y='Close', title=default_symbol)

def test_func(x, dist, amp, omega, phi):
    # For a sinusoidal model: https://towardsdatascience.com/fitting-cosine-sine-functions-with-machine-learning-in-python-610605d9b057
    return dist + amp * np.cos(omega * x + phi)

def convert_to_unix(date):
    '''
    Converts a datetime object to a UNIX timestamp (number)
    date: datetime obj
    '''
    unix = date.replace(tzinfo=timezone.utc).timestamp()
    return unix

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

    # Stock graph
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

    print(f'New stock searched: {value}')
    print(df.head())

    # Creating figure
    f = px.line(df, x=df.index, y=price, title=value)

    if model=='True':
        print('Generating model...')

    return [f, df.head(n=10).to_dict('records')]
    

# Run the app
if __name__ == "__main__":
    app.run_server(debug=True)


# TODO:

#    -Add symbol lookup (Check Finnhub's function: https://finnhub.io/docs/api/symbol-search)
#    -



