import alpaca_trade_api as tradeapi
import json
import os
import requests

APCA_API_BASE_URL = os.getenv("APCA_API_BASE_URL")
APCA_API_KEY_ID = os.getenv("APCA_API_KEY_ID")
APCA_API_SECRET_KEY = os.getenv("APCA_API_SECRET_KEY")

ACCOUNT_URL = "{}/v2/account".format(APCA_API_BASE_URL)

ORDERS_URL = "{}/v2/orders".format(APCA_API_BASE_URL)

CANCEL_ALL_ORDERS = "{}/v2/orders".format(APCA_API_BASE_URL)


POSITIONS_URL = "{}/v2/positions".format(APCA_API_BASE_URL)


HEADERS = {'APCA-API-KEY-ID': APCA_API_KEY_ID,
           'APCA-API-SECRET-KEY': APCA_API_SECRET_KEY
           }


api = tradeapi.REST(APCA_API_KEY_ID,
                    APCA_API_SECRET_KEY,
                    APCA_API_BASE_URL,
                    api_version='v2'
                    )

####### ALPACA FUNCTIONS ########


def get_account():
    """Gets your accound using Account URL

    Returns:
        json -- outputs account information
    """
    r = requests.get(ACCOUNT_URL, headers=HEADERS)

    return json.loads(r.content)


def create_order(symbol, qty, side, Type, time_in_force):
    data = {
        "symbol": symbol,
        "qty": qty,
        "side": side,
        "Type": Type,
        "time_in_force": time_in_force
    }
    r = requests.post(ORDERS_URL, json=data, headers=HEADERS)

    return json.loads(r.content)


def cancel_all_orders():
    r = requests.delete(CANCEL_ALL_ORDERS, headers=HEADERS)
    return json.loads(r.content)


# Cancel a specific order,, need order id
'''
def cancel_individual_order(order_id):
    CANCEL_SPECIFIC_ORDER = "{}/v2/orders/{}".format(APCA_API_BASE_URL)
    r = requests.delete()
'''


def get_individual_position(stock):
    INDIVIDUAL_POSITION_URL = "{}/v2/positions/{}".format(
        APCA_API_BASE_URL, stock.upper())
    r = requests.get(INDIVIDUAL_POSITION_URL, headers=HEADERS)

    return json.loads(r.content)


def get_positions():
    r = requests.get(POSITIONS_URL, headers=HEADERS)

    return json.loads(r.content)


def get_orders():
    r = requests.get(ACCOUNT_URL, headers=HEADERS)

    return json.loads(r.content)


def liquidate_account():
    r = requests.delete(POSITIONS_URL, headers=HEADERS)

    return json.loads(r.content)


def liquidate_position(stock):
    LIQUIDATE_POSITION = "{}/v2/positions/{}".format(
        APCA_API_BASE_URL, stock.upper())
    r = requests.delete(LIQUIDATE_POSITION, headers=HEADERS)

    return json.loads(r.content)


def account_activities(activity):
    account_activity = f"{APCA_API_BASE_URL}/v2/account/activities/{activity}"
    r = requests.get(account_activity, headers=HEADERS)

    return json.loads(r.content)

#### Example Calls ####

#response2 = create_order("AAPL", 100, "buy", "market", "gtc")
#stock = 'udow'
#position = get_individual_position(stock)
#position = get_positions()

#print(position)

# sell_order = liquidate_account()
# print(sell_order)
#stock = 'ino'

#sell_order = liquidate_position(stock)
#print(sell_order)

# sell_order = liquidate_account()
# print(sell_order)
#response = create_order("SVXY", 1, "buy", "market", "gtc")
#print(response)

#orders = get_orders()
#cancellations = cancel_all_orders()
#print(cancellations)

#print(response2)
#print(response)
