import yfinance as yf
from datetime import datetime, timedelta
from dataclasses import dataclass
from dateutil.relativedelta import relativedelta
import numpy as np
import pandas as pd
from pandas import DataFrame, Timestamp
import matplotlib.pyplot as plt
from yahooquery import Screener
import time

import os

from dataclasses import dataclass
import yfinance as yf

def remove_extension(str):
  return str.replace(".csv", "")

@dataclass
class InstrumentPair:
  numerator:          pd.DataFrame
  denominator:        pd.DataFrame
  numerator_symbol:   str
  denominator_symbol: str

  def __init(self, numerator, denominator):
    self.numerator          = numerator['series']
    self.denominator        = denominator['series']
    self.numerator_symbol   = numerator['symbol']
    self.denominator_symbol = denominator['symbol']

  # gets the percentual change for the dataframe
  # and gets the difference of each row between the 2 instruments
  #   pair.denominator['Close'].pct_change() * 100
  # 0           NaN
  # 1     -0.624440
  # 2      0.987430
  # 3      0.711110
  # 4     -0.441308
  # to then get their absolute value
  # to then aggregate it into one
  def score(self):
    return self.aggregated_series().abs().sum()

  def aggregated_series(self):
    try: 
      return (self.numerator['Close'].pct_change() * 100) - (self.denominator['Close'].pct_change() *100)
    except ValueError: # TODO ValueError: attempt to get argmax of an empty sequence
      return pd.Series()

  def to_string(self):
    return f"{self.numerator_symbol} / {self.denominator_symbol}"

def list_files(directory):
    # Ensure the directory exists
    if os.path.exists(directory):
        # List all files and directories in 'directory'
        entries = os.listdir(directory)
        # Filter out directories, keep filenames only
        files = [entry for entry in entries if os.path.isfile(os.path.join(directory, entry))]
        return files
    else:
        return f"Directory '{directory}' does not exist."


filenames      = list_files("data/instruments")
total          = len(filenames)
increments     = 50
selected_pairs = pd.DataFrame({
  'pair':  [],
  'score': []
})
ranges = [[start, min(start + increments - 1, total)] for start in range(0, total, increments)]
selected_pairs.to_csv('data/selected_pairs.csv', index=False)

for range_set in ranges:
  pairs = []
  time.sleep(3)

  for numerator in filenames[range_set[0]:range_set[1]]:
    for denominator in filenames[range_set[0]:range_set[1]]:

      is_comparable_pair = (numerator != denominator)

      if is_comparable_pair:
        try:
          pair = InstrumentPair(pd.read_csv('data/instruments/' + numerator), pd.read_csv('data/instruments/' + denominator), remove_extension(numerator), remove_extension(denominator))
          pairs.append(pair)
        except pd.errors.EmptyDataError:
          True
  
  sorted_pairs = sorted(pairs, key=lambda x: x.score(), reverse=True)
  for top_pair in sorted_pairs[:3]:
    row = pd.DataFrame({
      'pair':  [top_pair.to_string()],
      'score': [top_pair.score()]
    })
    row.to_csv('data/selected_pairs.csv', mode='a', header=False, index=False)


