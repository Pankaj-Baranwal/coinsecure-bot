import coinsecure as cs
import collections
import datetime
from time import sleep
import sys
import numpy as np
import tg

# LOWEST AT WHICH PEOPLE WILLING TO SELL
previous_ask_rate = cs.getLowestAskRate()
# HIGHEST AT WHICH PEOPLE WILLING TO BUY
previous_bid_rate = cs.getHighestBidRate()

counter = 0
while True:
	# LOWEST
	current_ask_rate = cs.getLowestAskRate()
	# HIGHEST
	current_bid_rate = cs.getHighestBidRate()
	print ('Iteration #' + str(counter))
	counter = counter + 1
	print ('current ask rate = ' + str(current_ask_rate))
	print ('previous ask rate = ' + str(previous_ask_rate))
	print ('current bid rate = ' + str(current_bid_rate))
	print ('previous bid rate = ' + str(previous_bid_rate))
	if previous_ask_rate - current_ask_rate > 5000:
		print('BOT SENDING MESSAGE')
		tg.sendMessage('GOOD TIME TO BUY! PRICES = ' + str(current_ask_rate) + " BEFORE: " + str(previous_ask_rate))
		previous_ask_rate = current_ask_rate
	if current_bid_rate - previous_bid_rate > 5000:
		print('BOT SENDING MESSAGE')
		previous_bid_rate = current_bid_rate
		tg.sendMessage('GOOD TIME TO SELL! PRICES = ' + str(current_bid_rate)  + " BEFORE: " + str(previous_bid_rate))
	print ('')
	print ('----x----x----')
	print ('')
	sleep(3)