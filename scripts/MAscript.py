import requests
import pandas as pd

def stockpriceanalysis(stock.upper()):
    stockprices = requests.get(f"https://financialmodelingprep.com/api/v3/historical-price-full/{stock}?serietype=line")
    stockprices = stockprices.json()

#Parse the API response and select only last 5 days of prices
    stockprices = stockprices['historical'][-5:]

#Convert from dict to pandas datafram

    prices5 = []
    prices3 = []
    tally = 0
    count = 1
    index = 0
    while index < len(stockprices):
        for key in stockprices[index]:
            if count % 2 == 0:
                if tally > 1:
                    prices3.append(stockprices[index][key])
                    prices5.append(stockprices[index][key])
                    
                else:
                    prices5.append(stockprices[index][key])
                    tally += 1
            count += 1
        index += 1

    sma_5 = 0
    for i in prices5:
        sma_5 += i

    sma_5 = sma_5 / len(prices5)
    print("SMA5: ",sma_5)
    
    sma_3 = 0
    for i in prices3:
        sma_3 += i

    sma_3 = sma_3 / len(prices3)
    print("SMA3: ",sma_3)

    if (sma_3 > sma_5):
        print("Long")
    else:
        print("Short")

    
stockpriceanalysis('aapl')















