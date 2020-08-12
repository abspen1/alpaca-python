import alpaca_trade_api as tradeapi
from datetime import date
import os


api = tradeapi.REST(
    os.getenv("APCA_API_KEY_ID"),
    os.getenv("APCA_API_SECRET_KEY"),
    os.getenv("APCA_API_BASE_URL"),
    api_version="v2",
)


short_list = []
cant_short_list = []
vol_short = []
vol_cant_short = []
watchlist = ['tqqq', 'spxl', 'tmf', 'edz', 'svxy']
volatility = ['VXX', 'UVXY']

def check_lists():
    for stock in watchlist:
        asset_info = api.get_asset(stock.upper())
        if asset_info.tradable:
            #print("We can trade {}.".format(stock.upper()))
            if asset_info.shortable:
                short_list.append(stock.upper())
            else:
                cant_short_list.append(stock.upper())
        #if asset_info.easy_to_borrow:
            #print("{} is easy to borrow.\n".format(stock.upper()))
        #else:
            #print("{} is hard to borrow.\n".format(stock.upper()))
    for stock in volatility:
        asset_info = api.get_asset(stock.upper())
        if asset_info.tradable:
            #print("We can trade {}.".format(stock.upper()))
            if asset_info.shortable:
                print(f"We can short {stock}")
                vol_short.append(stock.upper())
            else:
                vol_cant_short.append(stock.upper())
    #print('Can short: {}\n'.format(vol_short))
    #print('Cant short: {}'.format(vol_cant_short))


def record_shortable_data(vol_short, vol_cant_short):
    print("Updating the data files")
    if not os.path.exists('shortable-data'):
        os.makedirs('shortable-data')
    today = str(date.today())
    for ticker in vol_short:
        file1 = open(f"shortable-data/{ticker}-data.txt", "a")  # append mode
        file1.write(today)
        file1.write(": Shortable\n")
        file1.close()
    for ticker in vol_cant_short:
        file2 = open(f"shortable-data/{ticker}-data.txt", "a")  # append mode
        file2.write(today)
        file2.write(": NotShortable\n")
        file2.close()


def combine_shortable_data(vol_short):
    print("Updating the combined-data file")

    if vol_short:
        today = str(date.today())
        file1 = open("shortable-data/combined-data.txt", "a")  # append mode
        file1.write(today)
        file1.write("\n")
        for ticker in vol_short:
            file1.write(ticker)
            file1.write(": Shortable   ")
        file1.write("\n")


def get_percent_shortable(window_length):
    count = float(len(open("shortable-data/combined-data.txt").readlines()))
    count /= 2
    percent = float(count / window_length)
    percent *= 100
    print("Vol has been shortable {:.2f}% of the time over the past {} trading days.".format(
        percent, window_length))


if __name__ == "__main__":
    check_lists()
    record_shortable_data(vol_short, vol_cant_short)
    combine_shortable_data(vol_short)
    count = float(len(open("shortable-data/TVIX-data.txt").readlines()))
    get_percent_shortable(count)
