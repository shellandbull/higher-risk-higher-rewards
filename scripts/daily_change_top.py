import yfinance as yf
import plotly.graph_objs as go
import pandas as pd

# Define the tickers
tickers = yf.Tickers('CXAI ZETA-USD')

# Get historical data for the last 2 months
data = tickers.history(period="2mo")

# Calculate the daily percentage change
percent_changes = data['Close'].pct_change() * 100

# Create traces for CXAI and ZETA-USD
cxai_trace = go.Scatter(
    x=percent_changes.index,
    y=percent_changes['CXAI'],
    mode='lines',
    name='CXAI Daily % Change'
)

zeta_usd_trace = go.Scatter(
    x=percent_changes.index,
    y=percent_changes['ZETA-USD'],
    mode='lines',
    name='ZETA-USD Daily % Change'
)

# Create the layout
layout = go.Layout(
    title='Daily Percentage Price Change Over the Last 2 Months',
    xaxis=dict(title='Date'),
    yaxis=dict(title='Percentage Change'),
    showlegend=True
)

# Combine the traces and layout into a figure
fig = go.Figure(data=[cxai_trace, zeta_usd_trace], layout=layout)

# Show the plot
fig.show()
