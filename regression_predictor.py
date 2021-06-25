# Sci-kit learn regression prediction for stock data


import numpy as np
import matplotlib.pyplot as plt
import pandas_datareader as web
import pandas as pd
import datetime as dt
from sklearn.linear_model import LinearRegression
from sklearn import svm
from sklearn.model_selection import train_test_split


#knn = KNeighborsClassifier()


# Data should be formatted as (n_samples, n_features)
# n_features len(df.columns)
# n_samples = len(df)
start = dt.datetime.now() - dt.timedelta(days=3*365)# dt.datetime(2000, 1, 1)
end = dt.datetime.now().date()
df = web.DataReader('AAPL', 'yahoo', start, end)

print('APPLE DATA')
print(df)
print(df.columns)

train_df = df.head(len(df) - 1)
X = df[['High', 'Low', 'Open', 'Volume', 'Adj Close']]
y = df['Close']
train_size = len(df)-1
X_train, X_test, y_train, y_test = train_test_split(X, y, train_size=train_size)



print(X_train, X_test, y_train, y_test)

model = LinearRegression()
model.fit(X_train, y_train)

#test_x = df.tail(1)[['High', 'Low', 'Open', 'Volume', 'Adj Close']]

predictions = model.predict(X_test)

print('Predicted Vals:', predictions)
print(len(predictions))

plt.scatter(y_test, predictions)
plt.xlabel('Actual Prices')
plt.ylabel('Predicted Prices')
plt.show()
