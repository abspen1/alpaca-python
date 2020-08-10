""" 
    Started collecting data May 01, 2020. This is to see how reliable shorting volatility can be when 
    implementing into an algorithm. Shorting volatility has proved to be the most effective strategy 
    while backtesting on Quantopian. If vol can be shorted more than 50% of the time come May 01, 2021 
    that would be fantastic.
"""
import alpaca_trade_api as tradeapi
import os
import redis
import schedule
import time


def main():
    """Main function that initializes variables and calls the other helper functions.
    """
    client = redis.Redis(host="10.10.10.1", port=6379,
                         password=os.getenv("REDIS_PASS"))
    api = tradeapi.REST(
        os.getenv("APCA_API_KEY_ID"),
        os.getenv("APCA_API_SECRET_KEY"),
        os.getenv("APCA_API_BASE_URL"),
        api_version="v2",
    )
    clock = api.get_clock()
    # Check if the market is open.. Will always be open at this time if the market is open at all this day.
    # Important to do this so that we don't get data when the market is closed.
    if clock.is_open:
        shortable = False
        volatility = ['VXX', 'UVXY']
        vol_short = []
        for stock in volatility:
            asset_info = api.get_asset(stock.upper())
            if asset_info.tradable and asset_info.shortable:
                vol_short.append(stock.upper())
        if vol_short:
            shortable = True
            update_shortable(client, vol_short)
        else:
            print("No vol is shortable today.")

        total = update_total(client, volatility)

        pct = get_pct_shortable(client, shortable, total)

        percent = "%"

        print("Vol has been shortable {:.2f}{} of the time over the past {} trading days.".format(
            pct, percent, total))
    else:
        print("The market is closed today.")


def update_shortable(client, vol_short):
    """Updates the redis variable if vol is shortable this day.

    Args:
        client (obj): redis client object
        vol_short (list): list of the shortable volatility etfs
    """
    for ticker in vol_short:
        print(f"{ticker} is shortable today.")
        client_var = f"{ticker}_short"
        val = client.hget("vol_short_days", client_var)
        new_value = 1.0
        if val:
            new_value = float(val) + 1.0

        client.hset('vol_short_days', client_var, str(new_value))


def update_total(client, volatility):
    """Updates the redis variable keeping track of the number of days we've checked each vol etf

    Args:
        client (obj): redis client object
        volatility (list): list of each volatility etf we're checking

    Returns:
        [float]: total number of trading days we've checked volatility
    """
    for ticker in volatility:
        client_var = f"{ticker}_short"
        val = client.hget("vol_total_days", client_var)
        new_value = 1.0
        if val:
            new_value = float(val) + 1.0
        client.hset('vol_total_days', client_var, str(new_value))
        total = float(client.hget('vol_total_days', client_var))
    return total


def get_pct_shortable(client, shortable, total):
    """ First will update the shortable variable within redis database if vol was shortable today, then
        calculates and returns the percentage of time at least one vol etf has been shortable since recording

    Args:
        client (obj): redis client object
        shortable (bool): whether or not volatility was shortable today
        total (float): number of total trading days since recording

    Returns:
        float: percentage of time at least one vol etf has been shortable since recording
    """
    tally = float(client.get('shortable_tally'))
    if shortable:
        tally += 1
        client.set('shortable_tally', str(tally))
    pct = float(tally / total)*100

    return pct


print(time.ctime())

# Run this daily shortly after market opens in case it is a shortened trading day.
schedule.every().day.at("09:10").do(main)

while True:
    schedule.run_pending()
    time.sleep(1)
