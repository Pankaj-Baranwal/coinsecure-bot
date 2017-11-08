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
import sys

sys.stdout.flush()
# 1 = increasing slope. -1 = decreasing slope.
# Slope calculated by (current - previous) rate. = 1 if increasing. = -1 if decreasing
ask_orders_slope = sys.argv[1]
bid_orders_slope = sys.argv[2]
print (ask_orders_slope)
print (bid_orders_slope)

min_dist_from_minmax = 800
min_diff_in_slope = 400
min_diff_bw_buysell = 3500
vol_to_spend = 8000

previous_ask_rate = 0
previous_bid_rate = 0

local_maxima = cs.getMax24Hrs()
local_minima = cs.getMin24Hrs()

previous_buy_rate = 0

counter = 0
while True:

	latest_ask_rate = cs.getAskOrders(_max = 1)
	latest_bid_rate = cs.getBidOrders(_max = 1)

	# In case some query failed to get executed
	if latest_ask_rate == -1 or latest_bid_rate == -1:
		print ("FAILED TO RUN API")
		sleep(5)
		continue
	
	previous_ask_rate = latest_ask_rate[0]['rate']
	previous_bid_rate = latest_bid_rate[0]['rate']
	break

while True:
	counter = counter + 1
	print ("Iteration #" + str(counter))
	latest_ask_rate = cs.getAskOrders(_max = 1)
	latest_bid_rate = cs.getBidOrders(_max = 1)

	# In case some query failed to get executed
	if latest_ask_rate == -1 or latest_bid_rate == -1:
		print ("FAILED TO RUN API")
		sleep(5)
		continue

	latest_ask_rate = latest_ask_rate[0]['rate']
	latest_bid_rate = latest_bid_rate[0]['rate']

	print("PREVIOUS ASK RATE = " + str(previous_ask_rate))
	print("LATEST ASK RATE = " + str(latest_ask_rate))
	print("ASK ORDER SLOPE = " + str(ask_orders_slope))

	# If you want to buy, consider this
	if ask_orders_slope == -1 and latest_ask_rate - local_minima > min_dist_from_minmax:
		# CHECK IF WE HAVE MONEY, IF YES: PLACE BUY ORDER
		inr_balance = cs.getUserINRBalance()
		if inr_balance > latest_ask_rate*0.001:
			if len(cs.getExistingBuyOrder()) == 0:
				print ("---------x---------x--------")
				print ("READY TO PLACE BUY ORDER AT RATE = " + str(latest_ask_rate))
				print(cs.placeNewBuyOrder(_rate = latest_ask_rate, _volume = vol_to_spend))
				local_maxima = previous_ask_rate
				previous_buy_rate = latest_ask_rate
				print ("---------x---------x--------")
		ask_orders_slope = 1
	difference_in_rates = latest_ask_rate - previous_ask_rate
	if difference_in_rates > min_diff_in_slope:
		previous_ask_rate = latest_ask_rate

	print("PREVIOUS BID RATE = " + str(previous_bid_rate))
	print("LATEST BID RATE = " + str(latest_bid_rate))
	print("BID ORDER SLOPE = " + str(bid_orders_slope))

	# If you want to sell, consider this
	if bid_orders_slope == 1 and local_maxima - latest_bid_rate > min_dist_from_minmax:
		# CHECK IF WE HAVE BTC, IF YES: PLACE SELL ORDER
		btc_balance = cs.getUserBTCBalance()
		if btc_balance > 0.001 and previous_buy_rate - latest_bid_rate > min_diff_bw_buysell:
			if len(cs.getExistingSellOrder()) == 0:
				print ("---------x---------x--------")
				print ("READY TO PLACE SELL ORDER AT RATE = " + str(latest_bid_rate))
				print(cs.placeNewSellOrder(_rate = latest_bid_rate, _volume = vol_to_spend))
				print ("---------x---------x--------")
				local_minima = previous_bid_rate
		bid_orders_slope = -1
	difference_in_rates = previous_bid_rate - latest_bid_rate
	if difference_in_rates > min_diff_in_slope:
		previous_bid_rate = latest_bid_rate
	sleep(5)