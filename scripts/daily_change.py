import yfinance as yf
import plotly.graph_objs as go
import pandas as pd

# Define the tickers
tickers = yf.Tickers('BTC-USD CRO-USD')

# Get historical data for the last 2 months
data = tickers.history(period="2mo")

# Calculate the daily percentage change
percent_changes = data['Close'].pct_change() * 100

# Create traces for BTC-USD and CRO-USD
btc_trace = go.Scatter(
    x=percent_changes.index,
    y=percent_changes['BTC-USD'],
    mode='lines',
    name='BTC-USD Daily % Change'
)

cro_trace = go.Scatter(
    x=percent_changes.index,
    y=percent_changes['CRO-USD'],
    mode='lines',
    name='CRO-USD Daily % Change'
)

# Highlight areas where BTC-USD outperforms CRO-USD and vice versa
btc_over_cro = go.Scatter(
    x=percent_changes.index,
    y=percent_changes['BTC-USD'],
    fill='tonexty',
    mode='none',
    fillcolor='rgba(255, 255, 0, 0.5)',
    name='BTC Gains Over CRO'
)

cro_over_btc = go.Scatter(
    x=percent_changes.index,
    y=percent_changes['CRO-USD'],
    fill='tonexty',
    mode='none',
    fillcolor='rgba(0, 0, 255, 0.5)',
    name='CRO Gains Over BTC'
)

# Create the layout
layout = go.Layout(
    title='Daily Percentage Price Change Over the Last 2 Months',
    xaxis=dict(title='Date'),
    yaxis=dict(title='Percentage Change'),
    showlegend=True
)

# Combine the traces and layout into a figure
fig = go.Figure(data=[btc_trace, cro_over_btc, cro_trace, btc_over_cro], layout=layout)

# Show the plot
fig.show()



