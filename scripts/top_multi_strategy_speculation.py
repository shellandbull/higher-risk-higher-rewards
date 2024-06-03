import yfinance as yf
import numpy as np
import plotly.graph_objs as go
import pandas as pd

# Fetch historical data
def fetch_data():
    data = yf.download("CXAI ZETA-USD", period="2mo")['Close']
    return data

# Calculate the portfolio value
def simulate_trading(data, initial_btc, initial_cro, trade_amount):
    btc_held = initial_btc
    cro_held = initial_cro
    portfolio_value = []

    # Iterate through the DataFrame by rows
    for i in range(1, len(data)):
        btc_price = data['CXAI'].iloc[i]
        cro_price = data['ZETA-USD'].iloc[i]
        
        # Calculate current portfolio value
        current_value = btc_held * btc_price + cro_held * cro_price
        portfolio_value.append(current_value)
        
        # Calculate yesterday's prices and today's prices change
        btc_price_yesterday = data['CXAI'].iloc[i - 1]
        cro_price_yesterday = data['ZETA-USD'].iloc[i - 1]
        
        btc_change = (btc_price - btc_price_yesterday) / btc_price_yesterday
        cro_change = (cro_price - cro_price_yesterday) / cro_price_yesterday
        
        # Determine if a trade should be made (trade_amount of the base value)
        if btc_change > cro_change:  # BTC did better, sell some BTC
            btc_to_trade = trade_amount * btc_held
            cro_received = btc_to_trade * btc_price / cro_price
            btc_held -= btc_to_trade
            cro_held += cro_received
        elif cro_change > btc_change:  # CRO did better, sell some CRO
            cro_to_trade = trade_amount * cro_held
            btc_received = cro_to_trade * cro_price / btc_price
            cro_held -= cro_to_trade
            btc_held += btc_received

    portfolio_value = pd.Series(portfolio_value)
    interpolated = portfolio_value.interpolate()
    return interpolated

# Main function to run the simulation
def main():
    initial_btc = 0.3
    initial_cro = 10000
    data = fetch_data()
    portfolio_value = simulate_trading(data, initial_btc, initial_cro, 0.5)
    portfolio_value_at_small_trades = simulate_trading(data, initial_btc, initial_cro, 0.1)
    portfolio_value_at_large_trades = simulate_trading(data, initial_btc, initial_cro, 0.8)
    trading_everything = simulate_trading(data, initial_btc, initial_cro, 1.0) 

    # Create 2D plot with Plotly
    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=data.index[1:],
        y=portfolio_value,
        mode='lines',
        name='Trading 50% at a time'
    ))

    fig.add_trace(go.Scatter(
        x=data.index[1:],
        y=portfolio_value_at_small_trades,
        mode='lines',
        name='Trading 10% at a time'
    ))

    fig.add_trace(go.Scatter(
        x=data.index[1:],
        y=portfolio_value_at_large_trades,
        mode='lines',
        name='Trading 80% at a time'
    ))

    fig.add_trace(go.Scatter(
        x=data.index[1:],
        y=trading_everything,
        mode='lines',
        name='Trading everything'
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
