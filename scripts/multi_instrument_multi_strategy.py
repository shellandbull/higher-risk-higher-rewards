import yfinance as yf
import numpy as np
import plotly.graph_objs as go
import pandas as pd

# Fetch historical data
def fetch_data(instruments="BTC-USD CRO-USD"):
    data = yf.download(instruments, start="2022-01-01", end="2023-03-01")['Close']
    return data

# Calculate the portfolio value
def simulate_trading(data, initial_first, initial_second, trade_amount, first_instrument='BTC-USD', second_instrument='CRO-USD'):
    first_held = initial_first
    second_held = initial_second
    portfolio_value = []

    # Iterate through the DataFrame by rows
    for i in range(1, len(data)):
        first_price = data[first_instrument].iloc[i]
        second_price = data[second_instrument].iloc[i]
        
        # Calculate current portfolio value
        current_value = first_held * first_price + second_held * second_price
        portfolio_value.append(current_value)
        
        # Calculate yesterday's prices and today's prices change
        first_price_yesterday = data[first_instrument].iloc[i - 1]
        second_price_yesterday = data[second_instrument].iloc[i - 1]
        
        first_change = (first_price - first_price_yesterday) / first_price_yesterday
        second_change = (second_price - second_price_yesterday) / second_price_yesterday
        
        # Determine if a trade should be made (trade_amount of the base value)
        if first_change > second_change:  # First instrument did better, sell some of the first instrument
            first_to_trade = trade_amount * first_held
            second_received = first_to_trade * first_price / second_price
            first_held -= first_to_trade
            second_held += second_received
        elif second_change > first_change:  # Second instrument did better, sell some of the second instrument
            second_to_trade = trade_amount * second_held
            first_received = second_to_trade * second_price / first_price
            second_held -= second_to_trade
            first_held += first_received

    return portfolio_value

# Main function to run the simulation and plot the results
def main():
    initial_btc = 0.5
    initial_cro = 10000
    initial_pypl = 100
    initial_tsla = 100

    data = fetch_data()
    paypal_tesla_data = fetch_data('PYPL-USD TSLA-USD')
    tesla_bitcoin_data = fetch_data('TSLA-USD BTC-USD')

    portfolio_value = simulate_trading(data, initial_btc, initial_cro, 0.5, 'BTC-USD', 'CRO-USD')
    trading_everything = simulate_trading(data, initial_btc, initial_cro, 1.0, 'BTC-USD', 'CRO-USD')

    paypal_tesla_portfolio = simulate_trading(paypal_tesla_data, initial_pypl, initial_tsla, 0.5, 'PYPL-USD', 'TSLA-USD')
    tesla_bitcoin_portfolio = simulate_trading(tesla_bitcoin_data, initial_tsla, initial_btc, 0.5, 'TSLA-USD', 'BTC-USD')

    # Create 2D plot with Plotly
    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=data.index[1:],
        y=portfolio_value,
        mode='lines',
        name='BTC/CRO Trading 50% at a time'
    ))

    fig.add_trace(go.Scatter(
        x=data.index[1:],
        y=trading_everything,
        mode='lines',
        name='BTC/CRO Trading everything'
    ))

    fig.add_trace(go.Scatter(
        x=paypal_tesla_data.index[1:],
        y=paypal_tesla_portfolio,
        mode='lines',
        name='PAYPAL/TESLA Trading 50% at a time'
    ))

    fig.add_trace(go.Scatter(
        x=tesla_bitcoin_data.index[1:],
        y=tesla_bitcoin_portfolio,
        mode='lines',
        name='TESLA/BTC Trading 50% at a time'
    ))

    fig.update_layout(
        title='Portfolio Value Over Time',
        xaxis_title='Date',
        yaxis_title='Portfolio Value (USD)',
        showlegend=True
    )

    fig.show()

# Run the main function
main()
