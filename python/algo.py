'''
A simple algorithm showing how diversification and rebalancing
can make dramatic improvements to volatility and returns.
Note that this trades in 3X leveraged ETFs to get increased returns.
The diversification however, keeps the volatility in check.
Stats since 2011: 
Annual Return: 33.636%
Beta: 1.59
Alpha: 0.10
Annual Volatility: 29.786%

Property of Tendie Town LLC. All rights reserved.
'''
# python algo.py
import alpaca_trade_api as tradeapi
import json
import os
import redis
import requests
import schedule
import time


def main():
    api = tradeapi.REST(
        os.getenv("APCA_API_KEY_ID"),
        os.getenv("APCA_API_SECRET_KEY"),
        os.getenv("APCA_API_BASE_URL"),
        api_version="v2",
    )
    clock = api.get_clock()
    PortfolioHistory = api.get_portfolio_history()
    print("Launching Falcon-One")

    if not clock.is_open:
       print("The market is closed right now.")
       return
    
    etfs = {
        'TLT': 0.3,    # Bonds
        'EEM': 0.03,     # Emerging Markets
        'SPY': 0.29,    # S&P 500 
        'QQQ': 0.28,   # NASDAQ 
        'DIA': 0.1,    # DOW 
    }

    already_purchased = []
    rebalance(api, etfs, already_purchased, 1)
    time.sleep(60*10)
    get_account_data()
    base_value = float(PortfolioHistory.base_value)
    account = api.get_account()
    get_total_data(base_value, account)


def rebalance(api, etfs, purchased, fails):
    print("We're going to rebalance.")

    orders = api.list_orders(status='open')
    open_orders = []

    if orders:
        for order in orders:
            open_orders.append(order.symbol)
            print(f"{order.symbol} is in our open orders")

    try:
        for stock, weight in etfs.items():
            if stock not in open_orders and stock not in purchased:
                order_target_percent(api, stock, weight)
                time.sleep(2)
                purchased.append(stock)
    except Exception as e:
        # Definitely overboard on the formatting here lol
        if fails < 5:
            if (fails - 1) % 10 == 0:
                print(f"{fails}st error encountered.. trying again.")
            elif (fails - 2) % 10 == 0:
                print(f"{fails}nd error encountered.. trying again.")
            elif (fails - 3) % 10 == 0:
                print(f"{fails}rd error encountered.. trying again.")
            else:
                print(f"{fails}th error encountered.. trying again.")

            fails += 1
            time.sleep(3)
            rebalance(api, etfs, purchased, fails)
        else:
            print(
                f"Algo failed the max number of times: 5\nHere is the error\n\n")
            print(e, "\n\n")


def order_target_percent(api, asset, target, limit_price=None, stop_price=None, style=None):
    APCA_API_BASE_URL = os.getenv("APCA_API_BASE_URL")
    APCA_API_KEY_ID = os.getenv("APCA_API_KEY_ID")
    APCA_API_SECRET_KEY = os.getenv("APCA_API_SECRET_KEY")

    ORDERS_URL = "{}/v2/orders".format(APCA_API_BASE_URL)

    HEADERS = {'APCA-API-KEY-ID': APCA_API_KEY_ID,
               'APCA-API-SECRET-KEY': APCA_API_SECRET_KEY
               }
    print(f"Lets get {target} of our portfolio holding {asset}")
    qty = get_asset_qty(api, target, asset)
    if target < 0:
        print("Short order put in.. why?")
    elif target == 0:
        response = liquidate_position(asset, HEADERS, APCA_API_BASE_URL)
        print(response)
    elif qty != 0:
        side = 'buy'
        if qty < 0:
            side = 'sell'
        print(f"Trying to {side} {abs(qty)} shares of {asset}")
        response = create_order(asset, abs(qty), side,
                                "market", "gtc", ORDERS_URL, HEADERS)
        print(response)
    else:
        print(f"Sufficiently leveraged in {asset}")


def get_asset_qty(api, target, asset):
    asset = str(asset)
    account = api.get_account()
    portfolio = api.list_positions()
    base_value = float(account.portfolio_value)
    qty = 0
    holding = False
    for position in portfolio:
        if position.symbol == asset:
            holding = True
            print(f"Currently holding {position.qty} shares of {asset}")
            qty = get_qty(float(position.current_price),
                          float(position.qty), base_value, target)
    if not holding:
        print(f"Not currently holding {asset}")
        barset = api.get_barset(asset.upper(), 'minute')
        asset_barset = barset[asset.upper()]
        price = asset_barset[-1].c
        print(price)
        qty = get_qty(price,
                      0, base_value, target)

    return qty


def get_account_data():
    api = tradeapi.REST(
        os.getenv("APCA_API_KEY_ID"),
        os.getenv("APCA_API_SECRET_KEY"),
        os.getenv("APCA_API_BASE_URL"),
        api_version="v2",
    )
    account = api.get_account()
    balance_change = float(account.equity) - float(account.last_equity)
    total_pct = (balance_change/float(account.last_equity))*100
    if total_pct >= 0:
        print(
            "Today's unrealized percent change is + {:.3f}%".format(total_pct))
    else:
        print(
            "Today's unrealized percent change is - {:.3f}%".format(abs(total_pct)))


def get_total_data(base_value, account):
    print(f"Base value of account is ${base_value}")
    current_val = float(account.portfolio_value)
    print(f"Current value of account is ${current_val}")
    print(f'Account Cash: {account.cash}')
    profit_loss_pct = float((current_val - base_value) / base_value) * 100
    if profit_loss_pct >= 0:
        print("Total p/l percent: +{:.2f}%".format(profit_loss_pct))
    else:
        print("Total p/l percent: {:.2f}%".format(profit_loss_pct))


def get_qty(price, qty, base, target):
    base *= target
    new_qty = base/price
    if new_qty+0.2 > new_qty:
        new_qty += 0.2
    new_qty = int(new_qty)
    print(f"Our new target qty is :{new_qty})")
    return new_qty - qty


def get_weight(price, qty, base):
    price *= qty
    weight = price / base

    return weight


def create_order(symbol, qty, side, Type, time_in_force, ORDERS_URL, HEADERS):
    data = {
        "symbol": symbol,
        "qty": qty,
        "side": side,
        "Type": Type,
        "time_in_force": time_in_force
    }
    r = requests.post(ORDERS_URL, json=data, headers=HEADERS)

    return json.loads(r.content)


def liquidate_position(stock, HEADERS, APCA_API_BASE_URL):
    LIQUIDATE_POSITION = "{}/v2/positions/{}".format(
        APCA_API_BASE_URL, stock.upper())
    r = requests.delete(LIQUIDATE_POSITION, headers=HEADERS)

    return json.loads(r.content)


print(time.ctime())

schedule.every().day.at("09:15").do(main)
schedule.every().day.at("14:58").do(get_account_data)

while True:
    schedule.run_pending()
    time.sleep(1)
