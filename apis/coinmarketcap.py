from numpy import fix
from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json
import os
import pandas as pd

class CoinMarketCap:

  def __init__(self):
    self.url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest'

  def get_prices(self, symbols, currency, fixed_prices={}):
    if 'USD' in symbols:
        mapped_symbols = ['USDT' if s == 'USD' else s for s in symbols]
    else:
        mapped_symbols = symbols
    for c, v in fixed_prices.items():
        mapped_symbols.remove(c)
    parameters = {
      'symbol':",".join(mapped_symbols),
      'convert': currency
    }
    headers = {
      'Accepts': 'application/json',
      'X-CMC_PRO_API_KEY': os.getenv("CMC_TOKEN_ACCESS"),
    }
    session = Session()
    session.headers.update(headers)

    try:
      response = session.get(self.url, params=parameters)
      data = json.loads(response.text)
      prices = fixed_prices
      for coin, values in data["data"].items():
          prices[coin] = values["quote"][currency]["price"]
      s = pd.Series(prices)
      if 'USD' in symbols:
        s['USD'] = s['USDT']
      if 'PSI' in symbols:
        s['PSI'] = 0.2
      return s
    except (ConnectionError, Timeout, TooManyRedirects) as e:
      print(e)

def main():
    cmc = CoinMarketCap()
    df = cmc.get_prices(["BTC","ETH"], "EUR")
    print(df)

if __name__ == '__main__':
    main()