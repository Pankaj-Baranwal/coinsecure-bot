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
from time import sleep

# 1 = increasing slope. -1 = decreasing slope.
# Slope calculated by (current - previous) rate. = 1 if increasing. = -1 if decreasing
ask_orders_slope = int(raw_input("ask_orders_slope"))
bid_orders_slope = int(raw_input("bid_orders_slope"))

previous_ask_rate = 0
previous_bid_rate = 0

while True:
	latest_ask_order = cs.getAskOrders(_max = 1)
	latest_bid_order = cs.getBidOrders(_max = 1)

	# In case some query failed to get executed
	if latest_ask_order == -1 or latest_bid_order == -1:
		sleep(5)
		continue
	previous_ask_rate = latest_ask_order[0]['rate']
	previous_bid_rate = latest_bid_order[0]['rate']
	break

while True:
	latest_ask_order = cs.getAskOrders(_max = 1)
	latest_bid_order = cs.getBidOrders(_max = 1)

	# In case some query failed to get executed
	if latest_ask_order == -1 or latest_bid_order == -1:
		sleep(5)
		continue

	# If you want to buy, consider this
	difference_in_rates = latest_ask_order[0]['rate'] - previous_ask_rate
	if ask_orders_slope == -1 and difference_in_rates > min_dist_from_minmax:
		# CHECK IF WE HAVE MONEY, IF YES: PLACE BUY ORDER
		inr_balance = cs.getUserINRBalance()
		if inr_balance > latest_ask_order[0]['rate']*0.001:
			if len(cs.getExistingBuyOrder()) == 0:
				cs.placeNewBuyOrder(_rate = latest_ask_order[0]['rate'], _volume = money_to_spend)
		ask_orders_slope = 1
	if difference_in_rates > min_diff_in_slope:
		previous_ask_rate = latest_ask_order[0]['rate']

	# If you want to sell, consider this
	difference_in_rates = previous_bid_rate - latest_bid_order[0]['rate']
	if bid_orders_slope == 1 and difference_in_rates > min_dist_from_minmax:
		# CHECK IF WE HAVE BTC, IF YES: PLACE SELL ORDER
		btc_balance = cs.getUserBTCBalance()
		if btc_balance > 0.001:
			if len(cs.getExistingSellOrder()) == 0:
				cs.placeNewSellOrder(_rate = latest_bid_order, _volume = vol_to_sell)
		bid_orders_slope = -1
	if difference_in_rates > min_diff_in_slope:
		previous_bid_rate = latest_bid_order[0]['rate']
	sleep(5)