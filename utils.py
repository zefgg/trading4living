import requests

def get_top_symbols(limit=20):
    url = "https://api.coingecko.com/api/v3/coins/markets"
    params = {"vs_currency": "usd", "order": "market_cap_desc", "per_page": limit, "page": 1}
    data = requests.get(url, params=params).json()
    symbols = [coin["symbol"].upper() + "/USDT" for coin in data]
    return symbols
