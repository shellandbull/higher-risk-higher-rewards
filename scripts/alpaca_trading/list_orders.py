import os
from alpaca.trading.client import TradingClient
from alpaca.trading.requests import GetOrdersRequest
from alpaca.trading.enums import OrderSide, QueryOrderStatus

trading_client = TradingClient(os.environ['ALPACA_PAPER_API_KEY'], os.environ['ALPACA_PAPER_API_SECRET'], paper=True)

# params to filter orders by
request_params = GetOrdersRequest(
                    status=QueryOrderStatus.OPEN,
                    side=OrderSide.SELL
                 )

# orders that satisfy params
orders = trading_client.get_orders(filter=request_params)

print(orders)
