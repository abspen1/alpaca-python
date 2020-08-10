import alpaca_trade_api as tradeapi
import os

api = tradeapi.REST(
    os.getenv("APCA_API_KEY_ID"),
    os.getenv("APCA_API_SECRET_KEY"),
    os.getenv("APCA_API_BASE_URL"),
    api_version="v2",
)


def get_holdings_data():
    account = api.get_account()
    portfolio = api.list_positions()
    base_value = float(account.portfolio_value)
    total_weight = 0
    for position in portfolio:
        print("{} shares of {}".format(position.qty, position.symbol))
        print("{} has a profit/loss of {}".format(position.symbol,
                                                  position.unrealized_pl))
        weight = abs(get_weight(float(position.current_price),
                                float(position.qty), base_value))
        print("{} has a weight of {}".format(position.symbol, weight))
        total_weight += weight
    print(f"Total account leverage is {total_weight}")


# Helper function
def get_weight(price, qty, base):
    price *= qty
    weight = price / base

    return weight


def get_account_data():
    account = api.get_account()
    balance_change = float(account.equity) - float(account.last_equity)
    total_pct = (balance_change/float(account.last_equity))*100
    print("\n\n")
    if total_pct >= 0:
        print(
            "Today's unrealized percent change is + {:.3f}%".format(total_pct))
    else:
        print(
            "Today's unrealized percent change is - {:.3f}%".format(abs(total_pct)))


def get_total_data():
    account = api.get_account()
    if os.getenv("APCA_API_BASE_URL") == "https://api.alpaca.markets":
        base_value = 2500
    else:
        base_value = 10000 # Make sure to have all paper accts base = 10k
    print(f"Base value of account is ${base_value}")
    current_val = float(account.portfolio_value)
    print(f"Current value of account is ${current_val}")
    print(f'Account Cash: {account.cash}')
    profit_loss_pct = float((current_val - base_value) / base_value) * 100
    if profit_loss_pct >= 0:
        print("Total p/l percent: +{:.2f}%".format(profit_loss_pct))
    else:
        print("Total p/l percent: {:.2f}%".format(profit_loss_pct))


if __name__ == "__main__":
    want_stock_data = False
    if want_stock_data:
        get_holdings_data()
    get_account_data()
    print("\n################\n")
    get_total_data()
