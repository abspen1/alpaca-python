
from pylivetrader.api import order_target, record, symbol
from logbook import Logger, StreamHandler
import sys
StreamHandler(sys.stdout).push_application()
log = Logger(__name__)
'''
A simple algorithm showing how diversification and rebalancing
can make dramatic improvements to volatility and returns.
Note that this algorithm incorporates shorting/longing volatility ETF
UVXY. Based on moving averages data whether to long or short.
'''
def initialize(context):
    """
    Called once at the start of the algorithm.
    """   
    
    # Here are any algorithm 'constants' we'll be using
    context.target_leverage = 1.0
    context.vix = symbol('TVIX') # UVXY
    
    context.SHORT = 0
    context.LONG = 0
    # Here are the ETFs we want to trade along with the weights 
    # Ensure they add to 1.00
    # Or if using UVXY make sure to remove EDZ
    
    #BEARISH MARKET
    context.bullish = {
        #symbol('TLT'): 0.4, # Daily 20+ Year Treasury Bull 3X Shares
        symbol('TMF'): 0.4,
        symbol('TLT'): 0.0,
        symbol('EET'): 0.1,  # Daily MSCI Emerging Markets Bear 3X Shares
        symbol('SPXL'): 0.25,  # Daily S&P 500 Bull 3X Shares
        symbol('TQQQ'): 0.25,  # Daily NASDAQ Bull 3x Shares
    }
    
    #BULLISH MARKET
    context.bearish = {
        symbol('TMF'): 0.1, # Daily 20+ Year Treasury Bull 3X Shares
        symbol('EET'): 0.1,  # Daily MSCI Emerging Markets Bear 3X Shares
        symbol('SPXL'): 0.4,  # Daily S&P 500 Bull 3X Shares
        symbol('TQQQ'): 0.4,  # Daily NASDAQ Bull 3x Shares
    }
   
    # Set commision model for Robinhood / Alpaca
    # Rebalance our portfolio to maintain target weights
    schedule_function(short_vix, 
                      date_rules.every_day(), 
                      time_rules.market_close(minutes = 78)
                     )
    
def short_vix(context, data):
    hist=data.history(context.vix, 'price', 5, '1d')
    # Full 5 day simple moving average
    sma_5 = hist.mean()
    # 3 day simple moving average
    sma_3 = hist[3:].mean()
    open_orders = get_open_orders()
    if sma_5 < sma_3:
        print(f"sma_3: {sma_3} > sma_5: {sma_5} so we're Bearish")
        context.LONG += 1
        if context.vix not in open_orders:
            for stock, weight in list(context.bearish.items()):
                order_target_percent(stock, weight*context.target_leverage)
            
    elif sma_5 >= sma_3:
        print(f"sma_3: {sma_3} <= sma_5: {sma_5} so we're Bullish")
        if context.vix not in open_orders:
            context.SHORT += 1
            if context.vix not in open_orders:
                for stock, weight in list(context.bullish.items()):
                    order_target_percent(stock, weight*context.target_leverage)
    record(leverage = context.account.leverage)
    print(("Days bearish:{}".format(context.LONG)))
    print(("Days bullish: {}".format(context.SHORT)))
