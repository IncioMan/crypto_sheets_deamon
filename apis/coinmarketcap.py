from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json
import os
import pandas as pd

class CoinMarketCap:

  def __init__(self):
    self.url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest'

  def get_prices(self, symbols, currency):
    parameters = {
      'symbol':",".join(symbols),
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
      prices = {}
      for coin, values in data["data"].items():
          prices[coin] = values["quote"][currency]["price"]
      s = pd.Series(prices)
      return s
    except (ConnectionError, Timeout, TooManyRedirects) as e:
      print(e)

def main():
    cmc = CoinMarketCap()
    df = cmc.get_prices(["BTC","ETH"], "EUR")
    print(df)

if __name__ == '__main__':
    main()