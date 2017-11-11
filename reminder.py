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

while True:
	# LOWEST
	current_ask_rate = cs.getLowestAskRate()
	# HIGHEST
	current_bid_rate = cs.getHighestBidRate()
	if previous_ask_rate - current_ask_rate > 5000:
		previous_ask_rate = current_ask_rate
		tg.sendMessage('GOOD TIME TO BUY! PRICES = ' + str(current_ask_rate))
	if current_bid_rate - previous_bid_rate > 5000:
		previous_bid_rate = current_bid_rate
		tg.sendMessage('GOOD TIME TO SELL! PRICES = ' + str(current_bid_rate))
	sleep(3)