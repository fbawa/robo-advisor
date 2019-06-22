# app/robo_advisor.py

import requests
import json
import csv
import os
from dotenv import load_dotenv
import datetime


load_dotenv() #> loads contents of the .env file into the script's environment


#information inputs

def to_usd (my_price):
    return "${0:.2f}".format(my_price)

api_key = os.environ.get("ALPHAVANTAGE_API_KEY")

while True:
    symbol = input("Please input a stock symbol:")
    request_url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={symbol}&apikey={api_key}"
    response = requests.get(request_url)
    #print(type(response)) # class requests.models.response
    #print(response.status_code) #200
    #print(response.text)
    if symbol in response.text:
        break
    else:
        print("Please try a valid stock symbol again")

parsed_response = json.loads(response.text)

last_refreshed = parsed_response["Meta Data"]["3. Last Refreshed"]

tsd = parsed_response["Time Series (Daily)"]

dates = list(tsd.keys())

last_day = dates[0]

last_close = tsd[last_day]["4. close"]

currentDT = datetime.datetime.now()


#maximum prices 
high_prices = []
low_prices = []

for date in dates:
    high_price = tsd[date]["2. high"]
    low_price = tsd[date]["3. low"]
    high_prices.append(float(high_price))
    low_prices.append(float(low_price))

recent_high = max(high_prices)
recent_low = min(low_prices)


#information outputs

csv_file_path = os.path.join(os.path.dirname(__file__), "data", "prices.csv")

csv_headers = ["timestamp", "open", "high", "low", "close", "volume"]

with open(csv_file_path, "w") as csv_file:
    writer = csv.DictWriter(csv_file, fieldnames=csv_headers)
    writer.writeheader() # uses fieldnames set above
    daily_prices = tsd[date]
    for date in dates:
        writer.writerow({
        "timestamp": date,
        "open": daily_prices["1. open"], 
        "high": daily_prices["2. high"], 
        "low": daily_prices["3. low"], 
        "close": daily_prices["4. close"], 
        "volume": daily_prices["5. volume"],
        })
    


print("-------------------------")
print("SELECTED SYMBOL: MSFT")
print("-------------------------")
print("REQUESTING STOCK MARKET DATA...")
print("REQUEST AT:" + str(currentDT.strftime("%Y-%m-%d %H:%M:%S")))
print("-------------------------")
print(f"LATEST DAY: {last_refreshed}")  
print(f"LATEST CLOSE: {to_usd(float(last_close))}")
print(f"RECENT HIGH: {to_usd(float(recent_high))}")
print(f"RECENT LOW: {to_usd(float(recent_low))}")
print("-------------------------")
print("RECOMMENDATION: BUY!")
print("RECOMMENDATION REASON: TODO")
print("-------------------------")
print(f"WRITING DATA TO CSV: {csv_file_path}...")
print("-------------------------")  
print("-------------------------")
print("HAPPY INVESTING!")
print("-------------------------")

