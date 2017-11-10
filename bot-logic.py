import coinsecure as cs
import datetime
from time import sleep
import sys
import numpy as np
import tg

sys.stdout.flush()

print ('Initializing')

min24Hrs = cs.getMin24Hrs()
max24Hrs = cs.getMax24Hrs()
difference_between_extremes = max24Hrs - min24Hrs

previous_slope_for_ask_orders = 0
previous_slope_for_bid_orders = 0

# We will be using exchange trade prices instead of bid/ask orders
n = 10
pastTrades = cs.getPastTrades(_max = n)
row = [a['ordType'] for a in pastTrades]
# Loop until we have at least one bid and ask trades
while 'bid' not in row:
	n = n + 10
	pastTrades = cs.getPastTrades(_max = n)
	row = [a['ordType'] for a in pastTrades]
previous_ask_rate = pastTrades[row.index('bid')]['rate']/cs.UNIT_RUPEE
previous_bid_rate = cs.getBidOrders(_max = 1)
previous_bid_rate = cs.getBidOrders(_max = 1)[0]['rate']*0.01
# previous_bid_rate = pastTrades[row.index('bid')]['rate']/cs.UNIT_RUPEE

list_of_peaks = [] #Stores previously encountered maximas and minimas
threshold_for_stability = 600 # Minimum recognizable difference between two consecutive trades
volume_to_spend = 0.022 # Amount of BTC to spend in one transaction
count_trades = 0 # How many trades has bot successfully done
checkFor = int(sys.argv[1]) # -1 if we need minima next, 1 if we need a maxima next
if checkFor == 1:
	previous_buy_rate = sys.argv[2] # previous rate at which we placed a buy order
else:
	previous_buy_rate = 0 # previous rate at which we placed a buy order
print ('Initial need = ' + str(checkFor))
threshold_for_profit = 6000 # Minimum difference between buy and corresponding sell
counter = 0 # Number of iterations

print ('Initialization complete!')

# buy = -1 as we are losing inr. sell = 1 as we are gaining inr
def place_ask_order():
	# if already_placed_buy_order_without_sell == 1:
	# 	volume_to_spend = 0.011
	global count_trades
	global checkFor
	global list_of_peaks
	inr_balance = cs.getUserINRBalance()
	if inr_balance > latest_ask_rate * volume_to_spend:
		buy_rate = previous_ask_rate + 250
		if latest_ask_rate < previous_ask_rate + 250:
			buy_rate = latest_ask_rate
		while cs.placeNewBuyOrder(_rate = buy_rate , _volume = volume_to_spend) == -1:
			pass
		list_of_peaks[-1][2] = 1
		# pending_orders.append([-1, previous_ask_rate, volume_to_spend])
		# volume_to_spend = 0.022
		# already_placed_buy_order_without_sell = 1
		# have_extra_btc_to_sell = 0
		count_trades = count_trades + 1
		checkFor = 1
		print ('SUCESSFULLY PLACED A BUY ORDER')
		tg.sendMessage('bot-logic.py **** SUCESSFULLY PLACED A BUY ORDER')
	else:
		print ('Not enough balance. Need ' + str(latest_ask_rate * volume_to_spend))

def place_sell_order():
	global count_trades
	global checkFor
	global list_of_peaks
	# if have_extra_btc_to_sell == 1:
	# 	volume_to_spend = 0.011
	if cs.getUserBTCBalance() >= volume_to_spend:
		sell_rate = previous_bid_rate - 250
		if latest_bid_rate > previous_bid_rate - 250:
			sell_rate = latest_bid_rate
		while cs.placeNewSellOrder(rate = sell_rate, _volume = volume_to_spend) == -1:
			pass
		list_of_peaks[-1][2] = 1
		# pending_orders.append([1, previous_bid_rate, volume_to_spend])
		count_trades = count_trades + 1
		# already_placed_buy_order_without_sell = 0
		checkFor = -1
		print ('SUCESSFULLY PLACED A SELL ORDER')
		tg.sendMessage('bot-logic.py **** SUCESSFULLY PLACED A SELL ORDER')
	else:
		print ('Not enough balance. Need 0.022 BTC')

while True:
	# Get latest completed trades
	n = 10
	pastTrades = cs.getPastTrades(_max = n)
	row = [a['ordType'] for a in pastTrades]
	while 'bid' not in row:
		n = n + 10
		pastTrades = cs.getPastTrades(_max = n)
		row = [a['ordType'] for a in pastTrades]
	latest_ask_rate = pastTrades[row.index('bid')]['rate']/cs.UNIT_RUPEE
	latest_bid_rate = cs.getBidOrders(_max = 1)
	latest_bid_rate = latest_bid_rate[0]['rate']*0.01
	
	print('Iteration Number #' + str(counter))
	counter = counter + 1
	print ('')
	if checkFor == -1:
		print ('Need a MINIMA')
	else:
		print ('Need a MAXIMA')

	difference_in_ask_rates = latest_ask_rate - previous_ask_rate
	difference_in_bid_rates = previous_bid_rate - latest_bid_rate
	if (previous_slope_for_ask_orders == -1 and difference_in_ask_rates > threshold_for_stability) or (previous_slope_for_bid_orders == 1 and difference_in_bid_rates > threshold_for_stability):
		print('Latest ask rate: ' + str(latest_ask_rate))
		print('Previous ask rate: ' + str(previous_ask_rate))
		print ('PREVIOUS SLOPE FOR ASK: ' + str(previous_slope_for_ask_orders))
		print ('')
		print('Latest bid rate: ' + str(latest_bid_rate))
		print('previous bid rate: ' + str(previous_bid_rate))
		print ('PREVIOUS SLOPE FOR BID: ' + str(previous_slope_for_bid_orders))
		print('')
	# Check if we have a minima
	if previous_slope_for_ask_orders == -1 and difference_in_ask_rates > threshold_for_stability:
		# Add the new minima to list
		list_of_peaks.append([-1, previous_ask_rate, 0])
		print ('FOUND A MINIMA')

		# Confirm that we needed a minima (Need to place a buy order)
		if checkFor == -1:
			# We will not place a buy order if current rate is too close to max24Hrs
			divisions = [min24Hrs, min24Hrs + difference_between_extremes/4.0, min24Hrs + difference_between_extremes/4.0 + difference_between_extremes/4.0, max24Hrs - difference_between_extremes/4.0, max24Hrs]
			if np.digitize(previous_ask_rate, divisions) < 4:
				print ('Ready to buy!')
				place_ask_order()
			else:
				print ('Danger Zone! Not the right range to buy in!')
		else:
			print ('Expecting a maxima, got minima')

	if difference_in_ask_rates > threshold_for_stability:
		previous_slope_for_ask_orders = 1
		previous_ask_rate = latest_ask_rate
	elif difference_in_ask_rates < -threshold_for_stability:
		previous_slope_for_ask_orders = -1
		previous_ask_rate = latest_ask_rate
	if previous_slope_for_bid_orders == 1 and difference_in_bid_rates > threshold_for_stability:
		print ('FOUND A MAXIMA')
		list_of_peaks.append([1, previous_bid_rate, 0])
		if checkFor == 1:
			divisions = [min24Hrs, min24Hrs + difference_between_extremes/4.0, min24Hrs + difference_between_extremes/4.0 + difference_between_extremes/4.0, max24Hrs - difference_between_extremes/4.0, max24Hrs]
			if np.digitize(previous_ask_rate, divisions) > 1:
				print ('Optimal range to sell!')
				if latest_bid_rate - previous_buy_rate > threshold_for_profit:
					place_sell_order()
				else:
					print('But Not enough margin since last buy. :/')

			else:
				print ('Danger Zone! Not the right range to sell in!')
		else:
			print ('Expecting a minima, got maxima')
	if difference_in_bid_rates > threshold_for_stability:
		previous_slope_for_bid_orders = -1
		previous_bid_rate = latest_bid_rate
	elif difference_in_bid_rates < -threshold_for_stability:
		previous_slope_for_bid_orders = 1
		previous_bid_rate = latest_bid_rate
	print('Completed orders: ' + str(count_trades))
	print('')
	print('-----x------x--------x-------')
	print('')
	sleep(5)


# # 1 = increasing slope. -1 = decreasing slope.
# # Slope calculated by (current - previous) rate. = 1 if increasing. = -1 if decreasing
# ask_orders_slope = sys.argv[1]
# bid_orders_slope = sys.argv[2]
# print (ask_orders_slope)
# print (bid_orders_slope)

# min_dist_from_minmax = 300
# min_diff_in_slope = 300
# min_diff_bw_buysell = 3500
# vol_to_spend = 0.02

# previous_ask_rate = 0
# previous_bid_rate = 0

# local_maxima = cs.getMax24Hrs()
# local_minima = cs.getMin24Hrs()

# previous_buy_rate = 0

# counter = 0
# while True:
# 	latest_ask_rate = cs.getAskOrders(_max = 1)
# 	latest_bid_rate = cs.getBidOrders(_max = 1)

# 	# In case some query failed to get executed
# 	if latest_ask_rate == -1 or latest_bid_rate == -1:
# 		print ("FAILED TO RUN API")
# 		sleep(5)
# 		continue
	
# 	previous_ask_rate = latest_ask_rate[0]['rate']*0.01
# 	previous_bid_rate = latest_bid_rate[0]['rate']*0.01
# 	break

# count_placed_orders = 0
# print ("MOVING TO ITERATIVE CODE")
# while True:
# 	print ('\n\n')
# 	counter = counter + 1
# 	print ("Iteration #" + str(counter))
# 	latest_ask_rate = cs.getAskOrders(_max = 1)
# 	latest_bid_rate = cs.getBidOrders(_max = 1)

# 	# In case some query failed to get executed
# 	if latest_ask_rate == -1 or latest_bid_rate == -1:
# 		print ("FAILED TO RUN API")
# 		sleep(5)
# 		continue

# 	latest_ask_rate = latest_ask_rate[0]['rate']*0.01
# 	latest_bid_rate = latest_bid_rate[0]['rate']*0.01

# 	print("PREVIOUS ASK RATE = " + str(previous_ask_rate))
# 	print("LATEST ASK RATE = " + str(latest_ask_rate))
# 	print("ASK ORDER SLOPE = " + str(ask_orders_slope))
# 	print('')

# 	# If you want to buy, consider this
# 	if ask_orders_slope == -1 and latest_ask_rate - local_minima > min_dist_from_minmax:
# 		# CHECK IF WE HAVE MONEY, IF YES: PLACE BUY ORDER
# 		inr_balance = cs.getUserINRBalance()
# 		print('')
# 		print ("INR BALANCE: " + str(inr_balance))
# 		if inr_balance > latest_ask_rate*0.001:
# 			if len(cs.getExistingBuyOrder()) == 0:
# 				print ("---------x---------x--------")
# 				print ("READY TO PLACE BUY ORDER AT RATE = " + str(latest_ask_rate))
# 				print(cs.placeNewBuyOrder(_rate = latest_ask_rate, _volume = vol_to_spend))
# 				count_placed_orders = count_placed_orders + 1
# 				local_maxima = previous_ask_rate
# 				previous_buy_rate = latest_ask_rate
# 				print ("---------x---------x--------")
# 	difference_in_rates = latest_ask_rate - previous_ask_rate
# 	if difference_in_rates > min_diff_in_slope:
# 		previous_ask_rate = latest_ask_rate
# 		ask_orders_slope = 1
# 	elif difference_in_rates < -min_diff_in_slope:
# 		previous_ask_rate = latest_ask_rate
# 		ask_orders_slope = -1

# 	print("PREVIOUS BID RATE = " + str(previous_bid_rate))
# 	print("LATEST BID RATE = " + str(latest_bid_rate))
# 	print("BID ORDER SLOPE = " + str(bid_orders_slope))

# 	# If you want to sell, consider this
# 	if bid_orders_slope == 1 and local_maxima - latest_bid_rate > min_dist_from_minmax:
# 		# CHECK IF WE HAVE BTC, IF YES: PLACE SELL ORDER
# 		btc_balance = cs.getUserBTCBalance()
# 		if btc_balance > 0.01 and previous_buy_rate - latest_bid_rate > min_diff_bw_buysell:
# 			if len(cs.getExistingSellOrder()) == 0:
# 				print ("---------x---------x--------")
# 				print ("READY TO PLACE SELL ORDER AT RATE = " + str(latest_bid_rate))
# 				print(cs.placeNewSellOrder(_rate = latest_bid_rate, _volume = vol_to_spend))
# 				count_placed_orders = count_placed_orders + 1
# 				print ("---------x---------x--------")
# 				local_minima = previous_bid_rate
# 	print ('Placed ORDERS = ' + str(count_placed_orders))
# 	difference_in_rates = previous_bid_rate - latest_bid_rate
# 	if difference_in_rates > min_diff_in_slope:
# 		previous_bid_rate = latest_bid_rate
# 		bid_orders_slope = -1
# 	elif difference_in_rates < -min_diff_in_slope:
# 		previous_bid_rate = latest_bid_rate
# 		bid_orders_slope = 1
# 	print('LOCAL Maxima = ')
# 	sleep(5)
