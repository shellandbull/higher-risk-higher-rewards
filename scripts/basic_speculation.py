import yfinance as yf
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

# Fetch historical data
def fetch_data():
    data = yf.download("BTC-USD CRO-USD", start="2023-01-01", end="2023-03-01")['Close']
    return data

# Calculate the portfolio value
def simulate_trading(data, initial_btc, initial_cro):
    btc_held = initial_btc
    cro_held = initial_cro
    portfolio_value = []

    # Iterate through the DataFrame by rows
    for i in range(1, len(data)):
        btc_price = data['BTC-USD'].iloc[i]
        cro_price = data['CRO-USD'].iloc[i]
        
        # Calculate current portfolio value
        current_value = btc_held * btc_price + cro_held * cro_price
        portfolio_value.append(current_value)
        
        # Calculate yesterday's prices and today's prices change
        btc_price_yesterday = data['BTC-USD'].iloc[i - 1]
        cro_price_yesterday = data['CRO-USD'].iloc[i - 1]
        
        btc_change = (btc_price - btc_price_yesterday) / btc_price_yesterday
        cro_change = (cro_price - cro_price_yesterday) / cro_price_yesterday
        
        # Determine if a trade should be made (50% of the base value)
        if btc_change > cro_change:  # BTC did better, sell 50% BTC
            btc_to_trade = 0.5 * btc_held
            cro_received = btc_to_trade * btc_price / cro_price
            btc_held -= btc_to_trade
            cro_held += cro_received
        elif cro_change > btc_change:  # CRO did better, sell 50% CRO
            cro_to_trade = 0.5 * cro_held
            btc_received = cro_to_trade * cro_price / btc_price
            cro_held -= cro_to_trade
            btc_held += btc_received

    return portfolio_value

# Main function to run the simulation
def main():
    initial_btc = 0.3
    initial_cro = 10000
    data = fetch_data()
    portfolio_value = simulate_trading(data, initial_btc, initial_cro)
    
    # Plotting the portfolio value
    plt.figure(figsize=(10, 6))
    plt.plot(data.index[1:], portfolio_value, label='Portfolio Value')
    plt.title('Portfolio Value Over Time')
    plt.xlabel('Date')
    plt.ylabel('Portfolio Value (USD)')
    plt.legend()
    plt.grid(True)
    plt.show()

# Run the main function
main()
