from apis.coinmarketcap import CoinMarketCap 
from apis.google_sheets import GoogleSheets
import os
from datetime import datetime

coins_to_exclude = ["LIQUIDITA'", "Total"]

sheet = GoogleSheets(os.getenv("SHEET_ID"))
print("-"*20)
print(datetime.now())
print("-"*20)

def update_tx_price():
    print("Retrieving coins from google sheet...")
    df = sheet.get_ranges("[Crypto] Transactions",[2,3,16])[1:]
    df.columns = ["given_coin","received_coin","value_eur"]
    df = df[(df.given_coin != 'EUR')&(df.received_coin != 'EUR')&(df.value_eur == '')]
    print(f"Retrieved coins from google sheet")
    print("-"*10)
    if len(df) == 0:
        print("No transactions need price")
        return
    print("Retrieving prices from CoinMarketCap...")
    cmc = CoinMarketCap()
    prices = cmc.get_prices(df.given_coin.tolist(), "EUR")
    print("Retrieved prices from CoinMarketCap")
    print("-"*10)
    print("Writing prices to Google Sheet...")
    for i, row in df.iterrows():
        print(1+i, prices[row.given_coin])
        sheet.write_to_range("[Crypto] Transactions", prices[row.given_coin], f"P{1+i}")
    print("Wrote prices to Google Sheet")

def update_current_prices():
    print("Retrieving coins from google sheet...")
    coins = sheet.get_range("Crypto",1)
    coins.columns = ["coin"]
    coins = coins[1:] #remove header
    coins = coins[~(coins.coin == "") & ~(coins.coin.isin(coins_to_exclude))]
    print(f"Retrieved coins from google sheet: [{','.join(coins.coin.values.tolist())}]")
    print("-"*10)
    #
    print("Retrieving prices from CoinMarketCap...")
    cmc = CoinMarketCap()
    coins_list = coins.coin.tolist()
    df = cmc.get_prices(coins_list, "EUR", fixed_prices={'KYVE':0})
    print("Retrieved prices from CoinMarketCap")
    print("-"*10)
    values = []
    for coin in coins.coin:
        values.append([df.at[coin]])
    print("Writing prices to Google Sheet...")
    sheet.write_to_range("Crypto", values, "C2:C")
    print("Wrote prices to Google Sheet")

def main():
    print("-"*20)
    print("Updating coin prices")
    print("-"*20)
    update_current_prices()
    print("-"*20)

if __name__ == '__main__':
    main()