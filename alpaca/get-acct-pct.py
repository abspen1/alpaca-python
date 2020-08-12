import alpaca_trade_api as tradeapi
import os

##### Possible Addition to webapp #####

api = tradeapi.REST(
    os.getenv("APCA_API_KEY_ID"),
    os.getenv("APCA_API_SECRET_KEY"),
    os.getenv("APCA_API_BASE_URL"),
    api_version="v2",
)


""" Get true account base value """

def get_base():
    activities = api.get_activities()
    base_value = 0
    for activity in activities:
        try:
            if activity.activity_type == 'CSR':
                base_value += float(activity.net_amount)
            elif activity.activity_type == 'CSD':
                print(activity.net_amount)
                base_value += float(activity.net_amount)
        except Exception as e:
            print(e)
    return base_value


def get_total_data(base_value):
    account = api.get_account()
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
    base_value = get_base()
    get_total_data(base_value)