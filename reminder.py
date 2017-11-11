import coinsecure as cs
import datetime
from time import sleep
import sys
import numpy as np
import tg

# LOWEST AT WHICH PEOPLE WILLING TO SELL
previous_ask_rate = cs.getLowestAskRate()
# HIGHEST AT WHICH PEOPLE WILLING TO BUY
previous_bid_rate = cs.getHighestBidRate()
bins = [440000.0, 445000.0, 450000.0, 455000.0, 460000.0, 465000.0, 470000.0, 475000.0, 480000.0, 485000.0, 490000.0, 495000.0]
previous_ask_bin = np.digitize([previous_ask_rate], bins)
previous_bid_bin = np.digitize([previous_bid_rate], bins)
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
	current_ask_bin = np.digitize([current_ask_rate], bins)
	current_bid_bin = np.digitize([current_bid_rate], bins)

	if previous_ask_bin != current_ask_bin:
		print('BOT SENDING MESSAGE')
		tg.sendMessage('NEW ASK PRICES = ' + str(current_ask_rate) + " BEFORE: " + str(previous_ask_rate))
		previous_ask_rate = current_ask_rate
		previous_ask_bin = current_ask_bin
	if previous_bid_bin != current_bid_bin:
		print('BOT SENDING MESSAGE')
		previous_bid_rate = current_bid_rate
		previous_bid_bin = current_bid_bin
		tg.sendMessage('NEW BID PRICES = ' + str(current_bid_rate)  + " BEFORE: " + str(previous_bid_rate))
	print ('')
	print ('----x----x----')
	print ('')
	sleep(3)
