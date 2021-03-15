# Stock data visualization dashboard
# Awesome-quent list of packages for fin data: https://github.com/wilsonfreitas/awesome-quant#data-sources

import os
import pandas as pd
import matplotlib.pyplot as plt
import pandas_datareader as web
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

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server # server needed for heroku deploy

start = dt.datetime(2000, 1, 1)
end = dt.datetime.now().date()


print('Getting stock data...')
default_symbol = 'AAPL'
ddf = web.DataReader(default_symbol, 'yahoo', start, end)

print(ddf)#.head())
f = px.line(ddf, x=ddf.index, y='Adj Close', title=default_symbol)

def test_func(x, dist, amp, omega, phi):
	# For a sinusoidal model: https://towardsdatascience.com/fitting-cosine-sine-functions-with-machine-learning-in-python-610605d9b057
    return dist + amp * np.cos(omega * x + phi)

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
						value='Adj Close'
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

			], className='two columns')

])

# Updating graph based on user input values
@app.callback(
	Output('stock-graph', 'figure'),
	[Input('lookup-stock', 'value'),
	 Input('price-selection', 'value'),
	 Input('date-selector', 'start_date'),
	 Input('date-selector', 'end_date'),
	 Input('model-selector', 'value')]
	)

def update_stock_graph(value, price, start_date, end_date, model):
	'''Lookup new stock prices with user input'''
	df = web.DataReader(value, 'yahoo', start_date, end_date)

	print(f'New stock searched {value}')
	print(df.head())

	# Creating figure
	f = px.line(df, x=df.index, y=price, title=value)

	if model=='True':
		print('Generating model...')

	return f


# Run the app
if __name__ == "__main__":
	app.run_server(debug=True)
