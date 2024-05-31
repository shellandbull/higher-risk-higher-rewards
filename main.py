import yfinance as yf
from datetime import datetime, timedelta
from dataclasses import dataclass
from dateutil.relativedelta import relativedelta
import numpy as np
import pandas as pd
from pandas import DataFrame, Timestamp
import matplotlib.pyplot as plt

@dataclass
class TimeSeriesAsset:
  ticker:  yf.Ticker
  amount:  float
  date:    Timestamp
  history: DataFrame

  def __init(self, ticker, amount, date, history):
    self.ticker  = ticker
    self.amount  = amount
    self.date    = date
    self.history = history

  def to_string(self):
    return f"{self.ticker.info['name']} amount {self.amount} on {self.date} total {self.total()}"

  def total(self):
    return self.amount * self.tickerPriceAtDate()

  def tickerPriceAtDate(self):
    return self.history.loc[self.date, 'Close']

  def series(self):
    return self.history.loc[self.date]

cryptos = {
  "BTC":  "BTC-USD",
  "CRO":  "CRO-USD",
  "USDC": "USDC-USD"
}

tickersSet = yf.Tickers(' '.join(list(cryptos.values())))
bitcoin    = tickersSet.tickers['BTC-USD']
cro        = tickersSet.tickers['CRO-USD']
usdc       = tickersSet.tickers['USDC-USD']
two_months_ago    = datetime.now() - relativedelta(months=2)
initialTimeSeries = TimeSeriesAsset(bitcoin, 1.0, Timestamp(year=2024, month=1, day=1), bitcoin.history(period="2month"))
assetTimeSeries   = np.array([initialTimeSeries])

for ticker in [bitcoin, cro, usdc]:
  data  = ticker.history(start=two_months_ago.strftime('%Y-%m-%d'))
  quote = data['Close'].iloc[-1]
  output_string = f"{ticker.info['name']}: Last Price = ${quote:.2f}"
  print(output_string)
  for idx, row in data.iterrows():
    newAssetTimeSeries = TimeSeriesAsset(ticker, 0.0, row.name, data)
    np.append(assetTimeSeries, newAssetTimeSeries)

