import json
import requests
from Constants import *
from time import sleep

def consumeGETRequests(_endpoint, _extras):
	_params = {"accept": "application/json"}.items() + _extras.items()
	try:
		r = requests.get(url = BASE_URL+_endpoint, params = _params)
	except requests.exceptions.RequestException as e:
		print("ERROR")
		print (e)
		return -1

	if r.status_code == 200:
		data = r.json()
		if data['success']:
			return data['message']
	else:
		data = r.json()
		print(data['message'])
		return -1
	print (r.text)
	return -1

def consumeUserGETRequests(_endpoint, _extras):
	_params = {"accept": "application/json"}.items() + _extras.items()
	try:
		r = requests.get(url = BASE_URL+_endpoint, params = _params, headers = {"Authorization" : API_KEY})
	except requests.exceptions.RequestException as e:
		print("ERROR")
		print (e)
		return -1
	if r.status_code == 200:
		data = r.json()
		if data['success']:
			return data['message']
	else:
		data = r.json()
		print(data['message'])
		return -1
	print (r.text)
	return -1

def modifyUserData(_endpoint, _extras):
	_params = {"accept": "application/json"}.items() + _extras.items()
	try:
		r = requests.put(url = BASE_URL+_endpoint, data = _params, headers = {"Authorization" : API_KEY})
	except requests.exceptions.RequestException as e:
		print("ERROR")
		print (e)
		return -1
	if r.status_code == 200:
		data = r.json()
		if data['success']:
			return data['message']
	else:
		data = r.json()
		print(data['message'])
		return -1
	print (r.text)
	return -1
'''
Output: An integer number
'''
def getLowestAskRate():
	data = consumeGETRequests(ENDPOINT_LOWEST_ASK_RATE, dict())
	while data == -1:
		sleep(5)
		data = consumeGETRequests(ENDPOINT_LOWEST_ASK_RATE, dict())
	return data['rate']/UNIT_RUPEE

'''
Output: An integer number
'''
def getHighestBidRate():
	data = consumeGETRequests(ENDPOINT_HIGHEST_BID_RATE, dict())
	while data == -1:
		sleep(5)
		data = consumeGETRequests(ENDPOINT_HIGHEST_BID_RATE, dict())
	return data['rate']/UNIT_RUPEE

'''
Output: An integer number
'''
def getMin24Hrs():
	data = consumeGETRequests(ENDPOINT_MIN24_HRS, dict())
	while data == -1:
		sleep(5)
		data = consumeGETRequests(ENDPOINT_MIN24_HRS, dict())
	return data['rate']/UNIT_RUPEE

'''
Output: An integer number
'''
def getMax24Hrs():
	data = consumeGETRequests(ENDPOINT_MAX24_HRS, dict())
	while data == -1:
		sleep(5)
		data = consumeGETRequests(ENDPOINT_MAX24_HRS, dict())
	return data['rate']/UNIT_RUPEE

'''
Output: JSON Array.
Sample Output:
[{u'vol': 1000000, u'rate': 37501000, u'ordType': u'ask', u'time': 1508679162490}, 
{u'vol': 20000000, u'rate': 37500000, u'ordType': u'ask', u'time': 1508678719998}]

'''
def getPastTrades(_max):
	data = consumeGETRequests(ENDPOINT_PAST_TRADES, {'max': _max})
	while data == -1:
		sleep(5)
		data = consumeGETRequests(ENDPOINT_PAST_TRADES, {'max': _max})
	return data
	

'''
BUY ORDERS
[{u'vol': 9800000, u'rate': 38450000}, {u'vol': 40100000, u'rate': 38490000}, {u'vol': 570500000, u'rate': 38500000}]
'''    
def getBidOrders(_max):
	data = consumeGETRequests(ENDPOINT_BID_ORDERS, {'max': _max})
	while data == -1:
		sleep(5)
		data = consumeGETRequests(ENDPOINT_BID_ORDERS, {'max': _max})
	return data

'''
SELL ORDERS
[{u'vol': 1000000, u'rate': 38270001}, {u'vol': 1300000, u'rate': 38270000}, {u'vol': 13500000, u'rate': 38267200}]

'''    
def getAskOrders(_max):
	data = consumeGETRequests(ENDPOINT_ASK_ORDERS, {'max': _max})
	while data == -1:
		sleep(5)
		data = consumeGETRequests(ENDPOINT_ASK_ORDERS, {'max': _max})
	return data

def placeNewSellOrder(_rate, _volume):
	data = modifyUserData(ENDPOINT_PLACE_NEW_SELL_ORDER, {"rate" : int(_rate * UNIT_RUPEE), "vol" : int(_volume * UNIT_BTC)})
	if data != -1:
		return 1
	return -1

def placeNewBuyOrder(_rate, _volume):
	data = modifyUserData(ENDPOINT_PLACE_NEW_BUY_ORDER, {"rate" : int(_rate * UNIT_RUPEE), "vol" : int(_volume * UNIT_BTC)})
	if data != -1:
		return 1
	return -1

def getExistingBuyOrders(_max):
	data = consumeUserGETRequests(ENDPOINT_USER_PENDING_BUY_ORDERS, {'max': _max})
	while data == -1:
		sleep(5)
		data = consumeUserGETRequests(ENDPOINT_USER_PENDING_BUY_ORDERS, {'max': _max})
	return data

def getExistingSellOrders(_max):
	data = consumeUserGETRequests(ENDPOINT_USER_PENDING_SELL_ORDERS, {'max': _max})
	while data == -1:
		sleep(5)
		data = consumeUserGETRequests(ENDPOINT_USER_PENDING_SELL_ORDERS, {'max': _max})
	return data

def getUserINRBalance():
	data = consumeUserGETRequests(ENDPOINT_USER_INR_BALANCE, dict())
	while data == -1:
		sleep(5)
		data = consumeUserGETRequests(ENDPOINT_USER_INR_BALANCE, dict())
	return data['rate']/UNIT_RUPEE

def getUserBTCBalance():
	data = consumeUserGETRequests(ENDPOINT_USER_BTC_BALANCE, dict())
	while data == -1:
		sleep(5)
		data = consumeUserGETRequests(ENDPOINT_USER_BTC_BALANCE, dict())
	return data['vol']/UNIT_BTC

# print(getLowestAskRate())
# print(getHighestBidRate())
# print(getMin24Hrs())
# print(getMax24Hrs())
# print (getPastTrades(_max = 20))
# print(placeNewSellOrder(_rate = 400000, _volume = 0.010))
# print(placeNewBuyOrder(_rate = 300000, _volume = 0.010))
# print (getAskOrders(_max = 5))
# print (getBidOrders(_max = 3))
# print (getExistingBuyOrders(_max = 1))
# print (getExistingSellOrders(_max = 1))
# print (getUserINRBalance())
# print (getUserBTCBalance())