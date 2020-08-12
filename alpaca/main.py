'''
    MAKE SURE TO SPECIFY WHICH API KEYS
'''
import json
# https: // github.com/alpacahq/alpaca-trade-api-python/blob/master/examples/long-short.py
# https: // pypi.org/project/pylivetrader/
import csv

import requests
import pandas as pd
import alpaca_trade_api as tradeapi
import time
import datetime
import math
import statistics
from datetime import date, timedelta
import os
from collections import defaultdict, Counter
import redis
from pytz import timezone
import schedule
import numpy as np

############# PLEASE DOBULE CHECK RECORD DATA BEFORE RUNNING ################
RECORD_DATA = False

want_stock_data = False

want_account_data = True

want_todays_data = False

APCA_API_BASE_URL = os.getenv("APCA_API_BASE_URL")
APCA_API_KEY_ID = os.getenv("APCA_API_KEY_ID")
APCA_API_SECRET_KEY = os.getenv("APCA_API_SECRET_KEY")

ACCOUNT_URL = "{}/v2/account".format(APCA_API_BASE_URL)

ORDERS_URL = "{}/v2/orders".format(APCA_API_BASE_URL)

CANCEL_ALL_ORDERS ="{}/v2/orders".format(APCA_API_BASE_URL)


POSITIONS_URL = "{}/v2/positions".format(APCA_API_BASE_URL)


HEADERS = {'APCA-API-KEY-ID': APCA_API_KEY_ID,
            'APCA-API-SECRET-KEY': APCA_API_SECRET_KEY
            }


api = tradeapi.REST(APCA_API_KEY_ID,
                        APCA_API_SECRET_KEY,
                        APCA_API_BASE_URL,
                        api_version='v2'
                        )
clock = api.get_clock()


#print(f"Date and time is {time.ctime()}")
# def order_target_percent(asset, target, limit_price=None, stop_price=None, style=None):
#     api.list_positions()

#     monday = date.today() + timedelta(days=1)
#     tuesday = date.today() + timedelta(days=2)
#     wednesday = date.today() + timedelta(days=3)
#     thursday = date.today() + timedelta(days=4)
#     friday = date.today() + timedelta(days=5)
#     days_of_week = [monday, tuesday, wednesday, thursday, friday]


#     i = 0
#     for day in days_of_week:
#         calendar = api.get_calendar(start=day, end=day)[0]
#         if str(calendar.date) == str(day) + " 00:00:00":
#             open_times[i] = str(calendar.open)
#             close_times[i] = str(calendar.close)
#         else:
#             print(f"Market is not open on {day}")
#         i += 1

#     print(open_times)
#     print(close_times)
    
    
# print(time.ctime())

'''
schedule.every().day.at("11:30").do(job)
while True:
    schedule.run_pending()
    time.sleep(1)
'''


def handle_data(datetime):
    clock = api.get_clock()
    isOpen = clock.is_open
    print(f"We're open: {isOpen}")
    openingTime = clock.next_open.replace(
        tzinfo=datetime.timezone.utc).timestamp()
    closingTime = clock.next_close.replace(tzinfo=datetime.timezone.utc).timestamp()
    print(f"closing time : {closingTime}")
    currTime = clock.timestamp.replace(tzinfo=datetime.timezone.utc).timestamp()
    print(f"current time: {currTime}")
    timeToClose = (closingTime - currTime)/(60)
    timeToOpen = (openingTime - currTime)
    print(f"Minutes til close : {(timeToClose)}")
    print(f"Minutes til open : {timeToOpen}")
    

    if timeToClose > (60*60*58):
        print("Open is more than 57 hours away!")
    
# handle_data(datetime)


def get_eastern_time():
    # define eastern timezone
    eastern = timezone('US/Eastern')
    fmt = '%Y-%m-%d %H:%M:%S %Z%z'
    # naive datetime
    naive_dt = datetime.datetime.now()

    # localized datetime
    loc_dt = datetime.datetime.now(eastern)
    print(f"Actual time: {naive_dt.strftime(fmt)}")
    # 2015-12-31 19:21:00
    print(f"Eastern time: {loc_dt.strftime(fmt)}")
    # 2015-12-31 19:21:00 EST-0500
#get_eastern_time()

#activities = api.get_activities()
#print(f'All activities: {activities}')
#port_hist = api.get_portfolio_history()
#print(f'Portfolio History: {port_hist}')

#print(positions)

portfolio = api.list_positions()



#current_holdings = []
#for position in portfolio:
#    if float(position.unrealized_pl) > 0:
#        print(f"{position.symbol} had a profit of {position.unrealized_pl}")
#print(current_holdings)
#print(portfolio)

##### Random Alpaca Executables #####
#prospects = ['W', 'SBAC', 'EVER', 'CWH', 'GTT', 'VIX', 'doggy', 'hi', 'AAPL', 'FB', 'BRK.A']
#can_buy = []
#active_assets = api.list_assets(status='active')


#prospects = check_tradable(active_assets)
#print(prospects)

def get_new_prospects():
    """This will read our CSV file called prospects.csv
    """
    numStocks = 0
    with open('new_prospects.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        prospectList = []
        for row in csv_reader:
            if line_count == 0:
                print("\t".join(row))
            elif row[0] not in prospectList:
                prospectList.append(row[0])
                numStocks += 1
                print(row[0])

            line_count += 1
    
    
    print(f"\n{numStocks} new prospects this week.")
    return prospectList
    # Change our flag back to false
#list_pros = get_new_prospects()
#print(list_pros)
def re_write_csv(prospectDict, weekDict):
    with open('prospects.csv', mode='w') as f:
        writer = csv.writer(f, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        fieldnames = ['stock', 'profitLoss', 'weeks']
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()

        for key, value in prospectDict.items():
            week = weekDict[key]
            writer.writerow({'stock': key, 'profitLoss': value, 'weeks': week})

def read_csv():
    totalpl = 0
    numStocks = 0
    with open('prospects.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        prospects = {}
        weeks = {}
        for row in csv_reader:
            if line_count == 0:
                print("\t".join(row))
                line_count += 1
            elif row[0] not in prospects:
                prospects[row[0]] = float(row[1])
                weeks[row[0]] = float(row[2])
            else:
                prospects[row[0]] += float(row[1])
                weeks[row[0]] += float(row[2])

            #print(f'\t{row["stock"]} had profit/loss of {row["profitLoss"]}.')
            line_count += 1

    i = 0
    for key, value in prospects.items():
        totalpl += value
        numStocks += 1
        week = weeks[key]
        print("{}\t{:.2f}\t\t{}".format(key, value, week))
        i += 1
    print(f"\n{numStocks} different stocks, total profit/loss of {totalpl}\n")
    re_write_csv(prospects, weeks)
prospects = ['TQQQ', 'SPXL', 'TMF', 'SVXY']
selling = prospects
#read_csv()
def write_to_csv(selling, prospectList, modeType):
    with open('prospects.csv', mode=modeType) as prospects:
        writer = csv.writer(prospects, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        for position in portfolio:
            if position.symbol in selling:
                writer.writerow([position.symbol, position.unrealized_pl, 1])
                if float(position.unrealized_pl) > 0:
                    print(f"{position.symbol} had a profit of {position.unrealized_pl}")
                elif float(position.unrealized_pl) < 0:
                    print(f"{position.symbol} had a loss of {position.unrealized_pl}")
                else:
                    print(f"{position.symbol} had no profit or loss.. smh.")
            else:
                writer.writerow([position.symbol, 0.0, 1])
#write_to_csv(selling, prospects, 'a')
#write_to_csv(selling, prospects, modeType)
## Account Info ##
account = api.get_account()
bars = api.get_barset("TLT", "minute", 1)
totalPrice = bars["TLT"][0].c
#print("TLT price: ", totalPrice)
TLTlow = totalPrice * 0.97
TLThigh = totalPrice * 1.03

#print(f"Condor should range from {TLTlow} to {TLThigh}")
randomDict = defaultdict(lambda:0)

randomDict["a"] = 10
randomDict["b"] = 5

#print(randomDict["a"])
#print(randomDict["b"])
#print(randomDict["c"])

randomDict["c"] = max(randomDict["c"], randomDict["c"] + randomDict["a"])

#if randomDict["c"] > 0:
#    print(f'it worked {randomDict["c"]}')


'''
    Log of when vol is shortable:
        Apr
        May - 12
    
    Log of when vol isn't shortable:
        May - 1-12th
'''
# Get account total percent +/-
#curr_value = float(account.portfolio_value)
#print(type(int(curr_value)))
#account_ttl_pct_change = float(((curr_value - 100000) / 100000) *100)
#print("Total account percent change all-time: {}%".format(account_ttl_pct_change))
'''
balance_change = (float(account.equity) - float(account.last_equity))
print(f'Today\'s portfolio balance change: ${balance_change}')

total_equity = account.equity
print('${} is available as buying power.'.format(account.buying_power))
print('${} is my total portfolio equity.'.format(account.equity))

day_trade = account.daytrading_buying_power
print(f'Daytrade Buying Power: {day_trade}')

## Market Info ##
clock = api.get_clock()
print('The market is {}'.format('open.' if clock.is_open else 'closed.'))

date = '2020-04-23'
calendar = api.get_calendar(start=date, end=date)[0]
print('The market opened at {} and closed at {} on {}.'.format(
    calendar.open,
    calendar.close,
    date
))

'''
## Asset Info ##
'''
active_assets = api.list_assets(status='active')
nasdaq_assets = [a for a in active_assets if a.exchange == 'NASDAQ']
print(nasdaq_assets)
random_stock = 'FB'
random_asset = api.get_asset(random_stock)
if random_asset.tradable:
    print("We can trade {}.".format(random_stock))
'''
#stock_id = 'fb'
#stock_id = 'vxx'
#stock_id = 'qqq'
#stock_id = 'msft'
stock_id = 'qqq'

#print("Account has shorting enabled: {}\n".format(account.shorting_enabled))

#get_data_from_web()

'''
asset_info = api.get_asset(stock_id.upper())
if asset_info.tradable:
    print("We can trade {}.".format(stock_id))
    if asset_info.shortable:
        print("We can short {}.".format(stock_id))
    else:
        print("{} is not shortable.".format(stock_id))
    if asset_info.easy_to_borrow:
        print("{} is easy to borrow.".format(stock_id))
    else:
        print("{} is hard to borrow.".format(stock_id))
    if asset_info.marginable:
        print("{} is marginable.\n".format(stock_id))
    else:
        print('{} is not marginable.\n'.format(stock_id))

stock_id2 = 'tqqq'
print("Account has shorting enabled: {}".format(account.shorting_enabled))

asset_info = api.get_asset(stock_id2.upper())
if asset_info.tradable:
    print("We can trade {}.".format(stock_id2))
    if asset_info.shortable:
        print("We can short {}.".format(stock_id2))
    else:
        print("{} is not shortable.".format(stock_id2))
    if asset_info.easy_to_borrow:
        print("{} is easy to borrow.".format(stock_id2))
    else:
        print("{} is hard to borrow.".format(stock_id2))
    if asset_info.marginable:
        print("{} is marginable.".format(stock_id2))
    else:
        print('{} is not marginable.'.format(stock_id2))
'''
# Check on our positions, get a list of all of our positions.



PortfolioHistory = api.get_portfolio_history()
#profit_loss_pct = PortfolioHistory.profit_loss_pct
#base_value = PortfolioHistory.base_value


#for symbol in portfolio:
#position = api.get_position(symbol)
#    if int(symbol.qty) < 0:
#        print(f'Short position open for {symbol.symbol}')
#    else:
#        print(f'Long position open for {symbol.symbol}')
#        print(f'Total market value for {symbol.symbol} is {symbol.market_value}')


# Get the last 100 of our closed orders


if os.getenv("APCA_API_BASE_URL") == "https://api.alpaca.markets":
    base_value = 1500
elif os.getenv("APCA_API_KEY_ID") == "PK6JMZ1TJ7OZDCNKH6FS":
    base_value = 10000
else:
    base_value = float(PortfolioHistory.base_value)


# Print the quantity of shares for each position. and the profit/loss
portfolio = api.list_positions()


open_orders = api.list_orders(status='open')
if open_orders:
    print(f'All open orders {open_orders}')
    for order in open_orders:
        if order.symbol == 'SVXY':
            print(f"symbol -- {order.symbol}")
    closed_orders = api.list_orders(
        status='closed',
        limit=10
    )
else:
    print("No current open orders.")


def get_moving_average(stock_id, slow_len, fast_len):
    stock_id = stock_id.upper()

    barset_slow = api.get_barset(stock_id, 'day', limit=slow_len)
    barset_fast = api.get_barset(stock_id, 'day', limit=fast_len)
    stock_bars_slow = barset_slow[stock_id]
    stock_bars_fast = barset_fast[stock_id]

    # See how much Apple moved in that timeframe.
    #week_open = aapl_bars[0].o
    #week_close = aapl_bars[-1].c
    #percent_change = (week_close - week_open) / week_open * 100


    sma_slow = 0
    for i in range(len(stock_bars_slow)):
        sma_slow += stock_bars_slow[i].c
    sma_slow = sma_slow/len(stock_bars_slow)
    print("SMA5: ",sma_slow)

    sma_fast = 0                       
    for i in range(len(stock_bars_fast)):
        sma_fast += stock_bars_fast[i].c
    sma_fast = sma_fast/len(stock_bars_fast)
    print("SMA3: ",sma_fast)

    if sma_fast > sma_slow:
        print(f"{stock_id.upper()} is bullish\n")
    else:
        print(f"{stock_id.upper()} is bearish\n")




#moving_universe = ['tsla', 'qqq', 'spy', 'aapl', 'msft', 'ino', 'amd']
#stock_id = input('Please give me which stock to get 5/3 MA for: ' ).upper()
#for stock_id in moving_universe:
#    get_moving_average(stock_id, 100, 10)
stock_id = 'uvxy'
get_moving_average(stock_id, 5, 3)