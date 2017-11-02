'''
LOGIC:
Buying:
Buy orders will be placed only when the curve had a minima recently and now it has started to rise above a threshold range close to the minima.
Volume of the buy order will be prortional to the rate at which the price is increasing.
If the rate of increase is slow, smaller volume will be bought. Vice Versa.
There is an upper limit to the volume that can be bought in 1 transaction.


Selling:
Sell orders will be placed only when the curve had a maxima recently and now it has started to fall below a threshold range close to the maxima.
Volume of the sell order will be prortional to the rate at which the price is decreasing.
If the rate of decrease is slow, smaller volume will be sold. Vice Versa.
There is an upper limit to the volume that can be sold in 1 transaction.
Sell orders will be placed considering in mind that 0.4% is charged as interest by Coinsecure. Hence, the bot shouldn't sell at a price which results in a loss after deducting this amount.

Future:
Do we buy and sell at current rates or at a slightly modified rate?
'''
import coinsecure as cs
import datetime

# 1 = increasing slope. -1 = decreasing slope.
previous_ask_orders_slope = 0
current_ask_orders_slope = 0
previous_buy_orders_slope = 0
current_buy_orders_slope = 0
min_diff_in_slope = 500
min_dist_from_minmax = 1000
min_diff_bw_buysell = 2500
previous_maxima = 99999999
previous_minima = 0

# minima = cs.getMin24Hrs(_endpoint = "/exchange/min24Hr")
# maxima = cs.getMax24Hrs(_endpoint = "/exchange/max24Hr")

# while True:
# lowest = cs.getLowestAskRate(_endpoint = "/exchange/ask/low")
# highest = cs.getHighestBidRate(_endpoint = "/exchange/bid/high")
# min24 = cs.getMin24Hrs(_endpoint = "/exchange/min24Hr")
# max24 = cs.getMax24Hrs(_endpoint = "/exchange/max24Hr")
ask_orders = cs.getAskOrders(_endpoint = "/exchange/ask/orders", _max = 10)
bid_orders = cs.getBidOrders(_endpoint = "/exchange/bid/orders", _max = 10)
# If you want to buy, consider this
for x in ask_orders:
	difference_in_rates = previous['rate'] - x['rate']
	if difference_in_rates > min_diff_in_slope:
		if previous_ask_orders_slope == -1 and difference_in_rates > min_dist_from_minmax:
			
		previous_ask_orders_slope = current_ask_orders_slope
		current_ask_orders_slope = 1
	elif x['rate'] - previous['rate'] > min_diff_in_slope:
		ask_orders_slope = -1
# If you want to sell, consider this
# previous = buy_orders[0]
# for x in buy_orders:
# 	buy_orders_slope.append((previous['rate'] - x['rate'])/float(previous['time'] - x['time']))
# 	previous = x
print(ask_orders_slope)