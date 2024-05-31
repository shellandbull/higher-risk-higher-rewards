import yfinance as yf
import matplotlib.pyplot as plt
import pandas as pd

# Define the tickers
tickers = yf.Tickers('CXAI ZETA-USD')

# Get historical data for the last 2 months
data = tickers.history(period="2mo")

# Calculate the daily percentage change
percent_changes = data['Close'].pct_change() * 100

# Plotting
plt.figure(figsize=(14, 7))
for ticker in ['CXAI', 'ZETA-USD']:
    plt.plot(percent_changes.index, percent_changes[ticker], label=f'{ticker} Daily % Change')

# Find areas where CXAI outperforms ZETA-USD 
btc_over_cro = percent_changes['CXAI'] > percent_changes['ZETA-USD']
cro_over_btc = percent_changes['ZETA-USD'] > percent_changes['CXAI']

# Highlight non-overlapping areas where CXAI outperforms ZETA-USD 
plt.fill_between(percent_changes.index, percent_changes['CXAI'], percent_changes['ZETA-USD'], 
                 where=btc_over_cro, facecolor='darkgreen', alpha=0.5, interpolate=True,
                 label='BTC Gains Over CRO')

# Highlight non-overlapping areas where ZETA-USD  outperforms CXAI
plt.fill_between(percent_changes.index, percent_changes['ZETA-USD'], percent_changes['CXAI'], 
                 where=cro_over_btc, facecolor='darkred', alpha=0.5, interpolate=True,
                 label='CXAI Gains Over ZETA-USD')

plt.title('Daily Percentage Price Change Over the Last 2 Months')
plt.xlabel('Date')
plt.ylabel('Percentage Change')
plt.legend()
plt.grid(True)
plt.show()

