import requests

BASE_URL = "https://api.coinsecure.in/v1"
UNIT_RUPEE = 100
UNIT_BTC = 100000000
API_KEY = "ENTER_YOUR_API_KEY"

def consumeGETRequests(_endpoint, _extras):
	_params = {"accept": "application/json"}.items() + _extras.items()
	r = requests.get(url = BASE_URL+_endpoint, params = _params)
	data = r.json()
	return data

def modifyUserData(_endpoint, _extras):
	_params = {"accept": "application/json"}.items() + _extras.items()
	print (_params)
	# _header = _header_params
	r = requests.put(url = BASE_URL+_endpoint, data = _params, headers = {"Authorization" : API_KEY})
	data = r.json()
	return data

def getLowestAskRate(_endpoint):
	data = consumeGETRequests(_endpoint, dict())
	if data['success']:
		return data['message']['rate']
	else:
		return -1

def getHighestBidRate(_endpoint):
	data = consumeGETRequests(_endpoint, dict())
	if data['success']:
		return data['message']['rate']
	else:
		return -1

def getMin24Hrs(_endpoint):
	data = consumeGETRequests(_endpoint, dict())
	if data['success']:
		return data['message']['rate']
	else:
		return -1

def getMax24Hrs(_endpoint):
	data = consumeGETRequests(_endpoint, dict())
	if data['success']:
		return data['message']['rate']
	else:
		return -1

def getPastTrades(_endpoint, _max):
	data = consumeGETRequests(_endpoint, {'max': _max})
	if data['success']:
		return data['message']
	else:
		return -1

def placeNewSellOrder(_endpoint, _rate, _volume):
	data = modifyUserData(_endpoint, {"rate" : _rate * UNIT_RUPEE, "vol" : int(_volume * UNIT_BTC)})
	if data['success']:
		return 1
	else:
		return data

def placeNewBuyOrder(_endpoint, _rate, _volume):
	data = modifyUserData(_endpoint, {"rate" : _rate * UNIT_RUPEE, "vol" : int(_volume * UNIT_BTC)})
	if data['success']:
		return 1
	else:
		return data




# print(getLowestAskRate(_endpoint = "/exchange/ask/low"))
# print(getHighestBidRate(_endpoint = "/exchange/bid/high"))
# print(getMin24Hrs(_endpoint = "/exchange/min24Hr"))
# print(getMax24Hrs(_endpoint = "/exchange/max24Hr"))
# print (getPastTrades(_endpoint = "/exchange/trades", _MAX = 2))
# print(placeNewSellOrder(_endpoint = "/user/exchange/ask/new", _rate = 400000, _volume = 0.010))
# print(placeNewSellOrder(_endpoint = "/user/exchange/bid/new", _rate = 300000, _volume = 0.010))