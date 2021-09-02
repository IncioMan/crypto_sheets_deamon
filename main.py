from apis.coinmarketcap import CoinMarketCap 
from apis.google_sheets import GoogleSheets
import os

coins_to_exclude = ["LIQUIDITA'", "Total"]

sheet = GoogleSheets(os.getenv("SHEET_ID"))
print("-"*20)
#
print("Retrieving coins from google sheet...")
coins = sheet.get_range("Crypto",1)
coins.columns = ["coin"]
coins = coins[1:] #remove header
coins = coins[~(coins.coin == "") & ~(coins.coin.isin(coins_to_exclude))]
print(f"Retrieved coins from google sheet: [{','.join(coins.coin.values.tolist())}]")
print("-"*20)
#
print("Retrieving prices from CoinMarketCap...")
cmc = CoinMarketCap()
df = cmc.get_prices(coins.coin.tolist(), "EUR")
print("Retrieved prices from CoinMarketCap")
print("-"*20)
values = []
for coin in coins.coin:
    values.append([df.at[coin]])
print("Writing prices to Google Sheet...")
sheet.write_to_range("Crypto", values, "C6:C")
print("Wrote prices to Google Sheet")