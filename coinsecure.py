import json
import requests

BASE_URL = "https://api.coinsecure.in/v1"
UNIT_RUPEE = 100.0
UNIT_BTC = 100000000.0
# API_KEY = "ENTER_YOUR_API_KEY"
API_KEY = '9zzGq2WVcf08juU86qoizlbe7SPKs83fKFQmh9YK'

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
def getLowestAskRate(_endpoint):
	data = consumeGETRequests(_endpoint, dict())
	if data['success']:
		return data['message']['rate']
	return -1

'''
Output: An integer number
'''
def getHighestBidRate(_endpoint):
	data = consumeGETRequests(_endpoint, dict())
	if data['success']:
		return data['message']['rate']
	return -1

'''
Output: An integer number
'''
def getMin24Hrs(_endpoint):
	data = consumeGETRequests(_endpoint, dict())
	if data['success']:
		return data['message']['rate']
	return -1

'''
Output: An integer number
'''
def getMax24Hrs(_endpoint):
	data = consumeGETRequests(_endpoint, dict())
	if data['success']:
		return data['message']['rate']
	return -1

'''
Output: JSON Array.
Sample Output:
[{u'vol': 1000000, u'rate': 37501000, u'ordType': u'ask', u'time': 1508679162490}, 
{u'vol': 20000000, u'rate': 37500000, u'ordType': u'ask', u'time': 1508678719998}]

'''
def getPastTrades(_endpoint, _max):
	data = consumeGETRequests(_endpoint, {'max': _max})
	if data['success']:
		return data['message']
	return -1

'''
BUY ORDERS
[{u'vol': 9800000, u'rate': 38450000}, {u'vol': 40100000, u'rate': 38490000}, {u'vol': 570500000, u'rate': 38500000}]
'''    
def getBidOrders(_endpoint, _max):
	data = consumeGETRequests(_endpoint, {'max': _max})
	if (data['success']):
		return data['message']
	return -1;

'''
SELL ORDERS
[{u'vol': 1000000, u'rate': 38270001}, {u'vol': 1300000, u'rate': 38270000}, {u'vol': 13500000, u'rate': 38267200}]

'''    
def getAskOrders(_endpoint, _max):
	data = consumeGETRequests(_endpoint, {'max': _max})
	if (data['success']):
		return data['message']
	return -1;

def placeNewSellOrder(_endpoint, _rate, _volume):
	data = modifyUserData(_endpoint, {"rate" : _rate * UNIT_RUPEE, "vol" : int(_volume * UNIT_BTC)})
	if data['success']:
		return 1
	return data

def placeNewBuyOrder(_endpoint, _rate, _volume):
	data = modifyUserData(_endpoint, {"rate" : _rate * UNIT_RUPEE, "vol" : int(_volume * UNIT_BTC)})
	if (data['success']):
		return 1
	return data

def getExistingBuyOrders(_endpoint, _max):
	data = consumeUserGETRequests(_endpoint, {'max': _max})
	if (data['success']):
		return data['message']
	return -1

def getExistingSellOrders(_endpoint, _max):
	data = consumeUserGETRequests(_endpoint, {'max': _max})
	if (data['success']):
		return data['message']
	return -1

def getUserINRBalance(_endpoint):
	data = consumeUserGETRequests(_endpoint, dict())
	if data['success']:
		return data['message']['rate']/UNIT_RUPEE
	return -1

def getUserBTCBalance(_endpoint):
	data = consumeUserGETRequests(_endpoint, dict())
	if data['success']:
		return data['message']['vol']/UNIT_BTC
	return -1

# print(getLowestAskRate(_endpoint = "/exchange/ask/low"))
# print(getHighestBidRate(_endpoint = "/exchange/bid/high"))
# print(getMin24Hrs(_endpoint = "/exchange/min24Hr"))
# print(getMax24Hrs(_endpoint = "/exchange/max24Hr"))
# print (getPastTrades(_endpoint = "/exchange/trades", _max = 10))
# print(placeNewSellOrder(_endpoint = "/user/exchange/ask/new", _rate = 400000, _volume = 0.010))
# print(placeNewBuyOrder(_endpoint = "/user/exchange/bid/new", _rate = 300000, _volume = 0.010))
# print (getAskOrders(_endpoint = "/exchange/ask/orders", _max = 5))
# print (getBidOrders(_endpoint = "/exchange/bid/orders", _max = 3))
# print (getExistingBuyOrders(_endpoint = "/user/exchange/ask/pending", _max = 1))
# print (getExistingSellOrders(_endpoint = "/user/exchange/bid/pending", _max = 1))
# print (getUserINRBalance(_endpoint = "/user/exchange/bank/fiat/balance/available"))
# print (getUserBTCBalance(_endpoint = "/user/exchange/bank/coin/balance/available"))