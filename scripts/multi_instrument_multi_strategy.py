import yfinance as yf
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

# Fetch historical data
def fetch_data(instruments = "BTC-USD CRO-USD"):
    data = yf.download(instruments, start="2022-01-01", end="2023-03-01")['Close']
    return data

# Calculate the portfolio value
def simulate_trading(data, initial_btc, initial_cro, trade_amount, first_instrument='BTC-USD', second_instrument='CRO-USD'):
    btc_held = initial_btc
    cro_held = initial_cro
    portfolio_value = []

    # Iterate through the DataFrame by rows
    for i in range(1, len(data)):
        btc_price = data[first_instrument].iloc[i]
        cro_price = data[second_instrument].iloc[i]
        
        # Calculate current portfolio value
        current_value = btc_held * btc_price + cro_held * cro_price
        portfolio_value.append(current_value)
        
        # Calculate yesterday's prices and today's prices change
        btc_price_yesterday = data[first_instrument].iloc[i - 1]
        cro_price_yesterday = data[second_instrument].iloc[i - 1]
        
        btc_change = (btc_price - btc_price_yesterday) / btc_price_yesterday
        cro_change = (cro_price - cro_price_yesterday) / cro_price_yesterday
        
        # Determine if a trade should be made (50% of the base value)
        if btc_change > cro_change:  # BTC did better, sell 50% BTC
            btc_to_trade = trade_amount * btc_held
            cro_received = btc_to_trade * btc_price / cro_price
            btc_held -= btc_to_trade
            cro_held += cro_received
        elif cro_change > btc_change:  # CRO did better, sell 50% CRO
            cro_to_trade = trade_amount * cro_held
            btc_received = cro_to_trade * cro_price / btc_price
            cro_held -= cro_to_trade
            btc_held += btc_received

    return portfolio_value

# Main function to run the simulation
def main():
    initial_btc  = 0.5
    initial_cro  = 10000
    initial_pypl = 100
    initial_tsla = 100

    data               = fetch_data()
    paypal_tesla_data  = fetch_data('PYPL-USD TSLA-USD')
    tesla_bitcoin_data = fetch_data('TSLA-USD BTC-USD')

    plt.figure(figsize=(10, 6))

    portfolio_value = simulate_trading(data, initial_btc, initial_cro, 0.5, 'BTC-USD', 'CRO-USD')
    trading_everything = simulate_trading(data, initial_btc, initial_cro, 1.0, 'BTC-USD', 'CRO-USD')

    paypal_tesla_portfolio  = simulate_trading(paypal_tesla_data, initial_pypl, initial_tsla, 0.5, 'PYPL-USD', 'TSLA-USD')
    tesla_bitcoin_portfolio = simulate_trading(tesla_bitcoin_data, initial_tsla, initial_btc, 0.5, 'TSLA-USD', 'BTC-USD')
    
    # Plotting the portfolio value
    plt.plot(data.index[1:], portfolio_value, label="BTC/CRO Trading 50% at a time")
    plt.plot(data.index[1:], trading_everything, label="BTC/CRO Trading everything")
    plt.plot(data.index[1:], paypal_tesla_portfolio, label="PAYPAL/TESLA trading 50% at a time")
    plt.plot(data.index[1:], tesla_bitcoin_portfolio, label="TESLA/BTC trading 50% at a time")

    plt.title('Portfolio Value Over Time')
    plt.xlabel('Date')
    plt.ylabel('Portfolio Value (USD)')
    plt.legend()
    plt.grid(True)
    plt.show()

# Run the main function
main()
