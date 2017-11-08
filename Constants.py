from API import API_KEY

BASE_URL = "https://api.coinsecure.in/v1"
UNIT_RUPEE = 100.0
UNIT_BTC = 100000000.0

ENDPOINT_USER_BTC_BALANCE = "/user/exchange/bank/coin/balance/available"
ENDPOINT_USER_INR_BALANCE = "/user/exchange/bank/fiat/balance/available"
ENDPOINT_USER_PENDING_SELL_ORDERS = "/user/exchange/bid/pending"
ENDPOINT_USER_PENDING_BUY_ORDERS = "/user/exchange/ask/pending"
ENDPOINT_BID_ORDERS = "/exchange/bid/orders"
ENDPOINT_ASK_ORDERS = "/exchange/ask/orders"
ENDPOINT_PLACE_NEW_BUY_ORDER = "/user/exchange/bid/new"
ENDPOINT_PLACE_NEW_SELL_ORDER = "/user/exchange/ask/new"
ENDPOINT_PAST_TRADES = "/exchange/trades"
ENDPOINT_MAX24_HRS = "/exchange/max24Hr"
ENDPOINT_MIN24_HRS = "/exchange/min24Hr"
ENDPOINT_HIGHEST_BID_RATE = "/exchange/bid/high"
ENDPOINT_LOWEST_ASK_RATE = "/exchange/ask/low"