# app/robo_advisor.py

import requests
import json
import csv
import os
from dotenv import load_dotenv
import datetime
import finviz
import PySimpleGUI as sg

load_dotenv() #> loads contents of the .env file into the script's environment


#information inputs

def to_usd (my_price):
    return "${0:.2f}".format(my_price)

api_key = os.environ.get("ALPHAVANTAGE_API_KEY")

while True:
    symbol = sg.PopupGetText('Please input a stock symbol','Your Robo-Advisor')
    #symbol = input("Please input a stock symbol:")
    request_url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={symbol}&apikey={api_key}"
    response = requests.get(request_url)
    #print(type(response)) # class requests.models.response
    #print(response.status_code) #200
    #print(response.text)
    if symbol in response.text:
        break
    else:
        sg.Popup('Invalid stock symbol. Please try again')
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
    
#Recommendation

fin_viz = finviz.get_stock(symbol)
PE = str(fin_viz["P/E"])

if PE == "-":
    PE_format = 200
else:
    PE_format = float(PE)


if PE_format < 16.64:
    Recommendation = "Buy"
    Reason = "Company's current price to earnings ratio is below historical S&P 500 Average. As a result, we believe the company is undervalued"
else:
    Recommendation = "Hold or Sell"
    Reason = "Company's current price to earnings ratio is NOT below historical S&P 500 Average or company has no earnings. As a result, we believe the company is overvalued"

print("-------------------------")
print("SELECTED SYMBOL:" + str(symbol))
print("-------------------------")
print("REQUESTING STOCK MARKET DATA...")
print("REQUEST AT:" + str(currentDT.strftime("%Y-%m-%d %H:%M:%S")))
print("-------------------------")
print(f"LATEST DAY: {last_refreshed}")  
print(f"LATEST CLOSE: {to_usd(float(last_close))}")
print(f"RECENT HIGH: {to_usd(float(recent_high))}")
print(f"RECENT LOW: {to_usd(float(recent_low))}")
print("-------------------------")
print(f"PRICE-TO-EARNINGS RATIO: {PE}")
print(f"RECOMMENDATION: {Recommendation}")
print(f"RECOMMENDATION REASON: {Reason}")
print("-------------------------")
print(f"WRITING DATA TO CSV: {csv_file_path}...")
print("-------------------------")  
print("-------------------------")
print("HAPPY INVESTING!")
print("-------------------------")

#Graphic interface
sg.Popup("SELECTED SYMBOL:" + str(symbol),
"-------------------------",
"REQUESTING STOCK MARKET DATA...",
"REQUEST AT:" + str(currentDT.strftime("%Y-%m-%d %H:%M:%S")),
"-------------------------",
f"LATEST DAY: {last_refreshed}",  
f"LATEST CLOSE: {to_usd(float(last_close))}",
f"RECENT HIGH: {to_usd(float(recent_high))}",
f"RECENT LOW: {to_usd(float(recent_low))}",
"-------------------------",
f"PRICE-TO-EARNINGS RATIO: {PE}",
f"RECOMMENDATION: {Recommendation}",
f"RECOMMENDATION REASON: {Reason}",
"-------------------------",
f"WRITING DATA TO CSV: {csv_file_path}...",
"-------------------------",  
"-------------------------",
"HAPPY INVESTING!",
"-------------------------")