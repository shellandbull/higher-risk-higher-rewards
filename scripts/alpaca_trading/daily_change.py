import os
import yfinance as yf
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from alpaca.trading.client import TradingClient
from alpaca.trading.requests import GetAssetsRequest, MarketOrderRequest, GetOrdersRequest
from alpaca.trading.enums import AssetClass, OrderSide, TimeInForce


# ORDER TYPES 
# where should this information go?
# Market orders: Buy or sell immediately at the best available current price.
# Limit orders: Buy or sell at a specific price or better.
# Stop orders: Execute a buy or sell action once the price of the security reaches a specified price, known as the stop price.

trading_client = TradingClient(os.environ['ALPACA_PAPER_API_KEY'], os.environ['ALPACA_PAPER_API_SECRET'], paper=True)
positions = trading_client.get_all_positions()
bitcoin           = None
tesla             = None
placed_buy_order  = None
placed_sell_order = None

for pos in positions:
  if pos.symbol == 'BTCUSD':
    bitcoin = pos
  elif pos.symbol == 'TSLA':
    tesla = pos

if float(bitcoin.change_today) > float(tesla.change_today):
  bitcoin_qty_to_sell = float(bitcoin.qty_available) * 0.4
  tesla_qty_to_buy    = bitcoin_qty_to_sell * float(bitcoin.market_value) / float(tesla.current_price)

  placed_sell_order   = trading_client.submit_order(MarketOrderRequest(symbol="BTCUSD", qty=bitcoin_qty_to_sell, side=OrderSide.SELL, time_in_force=TimeInForce.GTC))
  placed_buy_order    = trading_client.submit_order(MarketOrderRequest(symbol="TSLA", qty=tesla_qty_to_buy, side=OrderSide.BUY, time_in_force=TimeInForce.DAY))
elif float(tesla.change_today) > float(bitcoin.change_today):
  tesla_qty_to_sell   = float(tesla.qty_available) * 0.4
  bitcoin_qty_to_buy  = tesla_qty_to_sell * float(tesla.market_value) / float(bitcoin.current_price)

  placed_sell_order   = trading_client.submit_order(MarketOrderRequest(symbol="TSLA", qty=tesla_qty_to_sell, side=OrderSide.SELL, time_in_force=TimeInForce.DAY))
  placed_buy_order    = trading_client.submit_order(MarketOrderRequest(symbol="BTCUSD", qty=bitcoin_qty_to_buy, side=OrderSide.BUY, time_in_force=TimeInForce.GTC))

print('------')
print('------')
print('------')
print('You bought')
print(placed_buy_order)
print('------')
print('------')
print('------')
print('You sold')
print(placed_sell_order)
