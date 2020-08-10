const dotenv = require("dotenv");
dotenv.config();

const API_KEY = process.env.APCA_API_KEY_ID;
const API_SECRET = process.env.APCA_API_SECRET_KEY;
const PAPER = true

class FalconOne {
    constructor(API_KEY, API_SECRET, PAPER) {
        this.Alpaca = require("@alpacahq/alpaca-trade-api");
        this.alpaca = new this.Alpaca({
        keyId: API_KEY,
        secretKey: API_SECRET,
        paper: PAPER,
        });
        // Example portfolio holdings with their respective weights
        this.stock1 = "TLT"; // BONDS ETF
        this.weight1 = 0.30;
        this.stock2 = "EEM"; // EMERGING MARKETS ETF
        this.weight2 = 0.10;
        this.stock3 = "QQQ"; // NASDAQ ETF
        this.weight3 = 0.25;
        this.stock4 = "DOW"; // DOW INDUSTRIAL ETF
        this.weight4 = 0.1;
        this.stock5 = "SPY"; // S&P 500 ETF
        this.weight5 = 0.25;
    }

    async run() {
        let i = 0
        let asset
        let weight
        let currentPrice
        let account = await this.alpaca.getAccount()
        // Get our account value
        const portfolioValue = account.portfolio_value;

        const portfolio = await this.alpaca.getPositions()
        do{
            i += 1;
            switch (i) {
                case 1:
                    asset = this.stock1;
                    weight = this.weight1;
                    break;
                case 2:
                    asset = this.stock2;
                    weight = this.weight2;
                    break;
                case 3:
                    asset = this.stock3;
                    weight = this.weight3;
                    break;
                case 4:
                    asset = this.stock4;
                    weight = this.weight4;
                    break;
                default:
                    asset = this.stock5;
                    weight = this.weight5;
                    break;
            }
            console.log(`\nRebalancing our holdings in ${asset}...\n`);

            let qty = await this.get_asset_qty(asset, portfolio);
            console.log(`Holding ${qty} shares of ${asset}`);
            if ( qty === 0 ) {
                currentPrice = await this.get_curr(asset)
            } else {
                currentPrice = await this.get_asset_curr(asset, portfolio);
            }
            console.log(`${asset}'s current price: ${currentPrice}`);
            qty = await this.get_qty(currentPrice, qty, portfolioValue, weight)
            await this.order_target(asset, weight, qty)
                 
        } while (i < 5)
        console.log("\nFinished running Falcon One\n")
        account = await this.alpaca.getAccount();
        console.log(`Portfolio's current value: ${account.portfolio_value}`)
        console.log(`Account Cash: ${account.cash}`);
        console.log(`Short Market Value: ${account.short_market_value}\n`);
    } // Finished run


    // Get the quantity of holdings in specific stock
    async get_asset_qty(asset, portfolio) {
        let qty = 0
        let holding = false
        // Print the quantity of shares for each position.
        portfolio.forEach(function (position) {
            if (position.symbol === asset) {
                // console.log(`${position.qty} shares of ${position.symbol}`);
                qty = position.qty
                holding = true
            }
        });
        if ( !holding ) {
            console.log(`Not currently holding ${asset}`);
            return qty
        }
        return qty
    }


    // Get current price of stock we dont hold
    async get_curr(asset) {
        var bars;
        await this.alpaca
          .getBars("minute", asset, { limit: 20 })
          .then((resp) => {
            bars = resp[asset];
          })
          .catch((err) => {
            console.log(err.error);
          });
        var currPrice = bars[bars.length - 1].closePrice;
        return currPrice
    }


    // Get current price of stock we hold
    async get_asset_curr(asset, portfolio) {
        let price = 0
        // Print the quantity of shares for each position.
        portfolio.forEach(function (position) {
            if (position.symbol === asset) {
                price = position.current_price;
            }
        });
        return price
    }


    // Get qty we want to order
    async get_qty(price, qty, val, target) {
        val *= target
        let newQty = val / price
        newQty += 0.2
        newQty = parseInt(newQty)
        console.log(`Our new target quantity is ${newQty}`)
        return (newQty - qty)
    }


    // Placing our orders
    async order_target(asset, target, qty) {
        console.log(`Let's get ${target} of our portfolio holding ${asset}`)
        if (target !== 0 && qty !== 0) {
            let side = 'buy'
            if (qty < 0) side = 'sell'
            qty = Math.abs(qty);
            console.log(`Trying to ${side} ${qty} shares of ${asset}`)
            await this.submitMarketOrder(asset, qty, side)
        } else console.log(`Sufficiently leveraged in ${asset}`)
        console.log("\n===================")
    }


    // Submit a market order if quantity is above 0.
    async submitMarketOrder(stock, quantity, side) {
        let errors = false
        if (quantity > 0) {
            let resp = await this.alpaca.createOrder({
                symbol: stock,
                qty: quantity,
                side: side,
                type: "market",
                time_in_force: "day",
            }).catch((err) => {
                console.log(
                    "Order of |" +
                    quantity +
                    " " +
                    stock +
                    " " +
                    side +
                    "| did not go through."
                    );
                    errors = true
                    console.log(err.message)
            });
            if ( !errors ){
                console.log(
                    "Market order of |" +
                    quantity +
                    " " +
                    stock +
                    " " +
                    side +
                    "| completed."
                    );
            }
        } else {
        console.log(
            "Quantity is <=0, order of |" +
            quantity +
            " " +
            stock +
            " " +
            side +
            "| not sent."
            );
        }
    }
}


// Run the Falcon One class.
var F1 = new FalconOne(API_KEY, API_SECRET, PAPER);
F1.run();