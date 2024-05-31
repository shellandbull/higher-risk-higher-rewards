import yfinance as yf
import matplotlib.pyplot as plt
import pandas as pd

# Define the tickers
tickers = yf.Tickers('BTC-USD CRO-USD')

# Get historical data for the last 2 months
data = tickers.history(period="2mo")

# Calculate the daily percentage change
percent_changes = data['Close'].pct_change() * 100

# Plotting
plt.figure(figsize=(14, 7))
for ticker in ['BTC-USD', 'CRO-USD']:
    plt.plot(percent_changes.index, percent_changes[ticker], label=f'{ticker} Daily % Change')

# Find areas where BTC-USD outperforms CRO-USD
btc_over_cro = percent_changes['BTC-USD'] > percent_changes['CRO-USD']
cro_over_btc = percent_changes['CRO-USD'] > percent_changes['BTC-USD']

# Highlight non-overlapping areas where BTC-USD outperforms CRO-USD
plt.fill_between(percent_changes.index, percent_changes['BTC-USD'], percent_changes['CRO-USD'], 
                 where=btc_over_cro, facecolor='darkgreen', alpha=0.5, interpolate=True,
                 label='BTC Gains Over CRO')

# Highlight non-overlapping areas where CRO-USD outperforms BTC-USD
plt.fill_between(percent_changes.index, percent_changes['CRO-USD'], percent_changes['BTC-USD'], 
                 where=cro_over_btc, facecolor='darkred', alpha=0.5, interpolate=True,
                 label='CRO Gains Over BTC')

plt.title('Daily Percentage Price Change Over the Last 2 Months')
plt.xlabel('Date')
plt.ylabel('Percentage Change')
plt.legend()
plt.grid(True)
plt.show()

