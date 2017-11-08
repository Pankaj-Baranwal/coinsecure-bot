import json
import requests
from Constants import *

def consumeGETRequests(_endpoint, _extras):
	_params = {"accept": "application/json"}.items() + _extras.items()
	try:
		r = requests.get(url = BASE_URL+_endpoint, params = _params)
	except requests.exceptions.ConnectionError:
		print("Connection refused")
		return -404
	data = r.json()
	return data

def consumeUserGETRequests(_endpoint, _extras):
	_params = {"accept": "application/json"}.items() + _extras.items()
	try:
		r = requests.get(url = BASE_URL+_endpoint, params = _params, headers = {"Authorization" : API_KEY})
	except requests.exceptions.ConnectionError:
		print("Connection refused")
		return -404
	data = r.json()
	return data

def modifyUserData(_endpoint, _extras):
	_params = {"accept": "application/json"}.items() + _extras.items()
	try:
		r = requests.put(url = BASE_URL+_endpoint, data = _params, headers = {"Authorization" : API_KEY})
	except requests.exceptions.ConnectionError:
		print("Connection refused")
		return -404
	data = r.json()
	return data
'''
Output: An integer number
'''
def getLowestAskRate():
	data = consumeGETRequests(ENDPOINT_LOWEST_ASK_RATE, dict())
	if data['success']:
		return data['message']['rate']
	return -1

'''
Output: An integer number
'''
def getHighestBidRate():
	data = consumeGETRequests(ENDPOINT_HIGHEST_BID_RATE, dict())
	if data['success']:
		return data['message']['rate']
	return -1

'''
Output: An integer number
'''
def getMin24Hrs():
	data = consumeGETRequests(ENDPOINT_MIN24_HRS, dict())
	if data['success']:
		return data['message']['rate']
	return -1

'''
Output: An integer number
'''
def getMax24Hrs():
	data = consumeGETRequests(ENDPOINT_MAX24_HRS, dict())
	if data['success']:
		return data['message']['rate']
	return -1

'''
Output: JSON Array.
Sample Output:
[{u'vol': 1000000, u'rate': 37501000, u'ordType': u'ask', u'time': 1508679162490}, 
{u'vol': 20000000, u'rate': 37500000, u'ordType': u'ask', u'time': 1508678719998}]

'''
def getPastTrades(_max):
	data = consumeGETRequests(ENDPOINT_PAST_TRADES, {'max': _max})
	if data['success']:
		return data['message']
	return -1

'''
BUY ORDERS
[{u'vol': 9800000, u'rate': 38450000}, {u'vol': 40100000, u'rate': 38490000}, {u'vol': 570500000, u'rate': 38500000}]
'''    
def getBidOrders(_max):
	data = consumeGETRequests(ENDPOINT_BID_ORDERS, {'max': _max})
	if (data['success']):
		return data['message']
	return -1;

'''
SELL ORDERS
[{u'vol': 1000000, u'rate': 38270001}, {u'vol': 1300000, u'rate': 38270000}, {u'vol': 13500000, u'rate': 38267200}]

'''    
def getAskOrders(_max):
	data = consumeGETRequests(ENDPOINT_ASK_ORDERS, {'max': _max})
	if (data['success']):
		return data['message']
	return -1;

def placeNewSellOrder(_rate, _volume):
	data = modifyUserData(ENDPOINT_PLACE_NEW_SELL_ORDER, {"rate" : _rate * UNIT_RUPEE, "vol" : int(_volume * UNIT_BTC)})
	if data['success']:
		return 1
	return data

def placeNewBuyOrder(_rate, _volume):
	data = modifyUserData(ENDPOINT_PLACE_NEW_BUY_ORDER, {"rate" : _rate * UNIT_RUPEE, "vol" : int(_volume * UNIT_BTC)})
	if (data['success']):
		return 1
	return data

def getExistingBuyOrders(_max):
	data = consumeUserGETRequests(ENDPOINT_USER_PENDING_BUY_ORDERS, {'max': _max})
	if (data['success']):
		return data['message']
	return -1

def getExistingSellOrders(_max):
	data = consumeUserGETRequests(ENDPOINT_USER_PENDING_SELL_ORDERS, {'max': _max})
	if (data['success']):
		return data['message']
	return -1

def getUserINRBalance():
	data = consumeUserGETRequests(ENDPOINT_USER_INR_BALANCE, dict())
	if data['success']:
		return data['message']['rate']/UNIT_RUPEE
	return -1

def getUserBTCBalance():
	data = consumeUserGETRequests(ENDPOINT_USER_BTC_BALANCE, dict())
	if data['success']:
		return data['message']['vol']/UNIT_BTC
	return -1

# print(getLowestAskRate())
# print(getHighestBidRate())
# print(getMin24Hrs())
# print(getMax24Hrs())
# print (getPastTrades(_max = 10))
# print(placeNewSellOrder(_rate = 400000, _volume = 0.010))
# print(placeNewBuyOrder(_rate = 300000, _volume = 0.010))
# print (getAskOrders(_max = 5))
# print (getBidOrders(_max = 3))
# print (getExistingBuyOrders(_max = 1))
# print (getExistingSellOrders(_max = 1))
# print (getUserINRBalance())
# print (getUserBTCBalance(_endpoint = "/user/exchange/bank/coin/balance/available"))