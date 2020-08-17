class algo {
    constructor(API_KEY, API_SECRET) {
        this.alpaca = new AlpacaCORS({
          keyId: API_KEY,
          secretKey: API_SECRET,
          baseUrl: "https://paper-api.alpaca.markets",
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
        await this.updatePositions();
        let i = 0;
        let asset;
        let weight;
        let currentPrice;
        let account = await this.alpaca.getAccount();
        // Get our account value
        const portfolioValue = account.portfolio_value;

        const portfolio = await this.alpaca.getPositions();
        do {
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
            

            let qty = await this.get_asset_qty(asset, portfolio);
            // writeToEventLog(`Holding ${qty} shares of ${asset}`);
            if (qty === 0) {
                currentPrice = await this.get_curr(asset);
            } else {
                currentPrice = await this.get_asset_curr(asset, portfolio);
            }
            qty = await this.get_qty(currentPrice, qty, portfolioValue, weight);
            await this.order_target(asset, weight, qty);
            writeToEventLog(`${asset}'s current price: ${currentPrice}`);
            writeToEventLog(`Rebalancing our holdings in ${asset}...\n`);
            writeToEventLog("\n===================");
        } while (i < 5);
        account = await this.alpaca.getAccount();
        writeToEventLog(`\nShort Market Value: ${account.short_market_value}\n`);
        writeToEventLog(`Account Cash: ${account.cash}`);
        writeToEventLog(`Portfolio's current value: ${account.portfolio_value}`);
        writeToEventLog("Finished running algo\n");
    } // Finished run

    // Get the quantity of holdings in specific stock
    async get_asset_qty(asset, portfolio) {
        let qty = 0;
        // Print the quantity of shares for each position.
        portfolio.forEach(function (position) {
        if (position.symbol === asset) {
            // writeToEventLog(`${position.qty} shares of ${position.symbol}`);
            qty = position.qty;
        }
        });
        return qty;
    }

    // Get current price of stock we dont hold
    async get_curr(asset) {
        var bars;
        var currPrice = new Promise(async (resolve, reject) => {
          await this.alpaca
            .getBars("minute", asset, { limit: 20 })
            .then((resp) => {
              resolve(resp[asset][0].c);
            })
            .catch((err) => {
              writeToEventLog(err);
            });
        });
        return currPrice;
    }

    // Get current price of stock we hold
    async get_asset_curr(asset, portfolio) {
        let price = 0;
        // Print the quantity of shares for each position.
        portfolio.forEach(function (position) {
        if (position.symbol === asset) {
            price = position.current_price;
        }
        });
        return price;
    }

    // Get qty we want to order
    async get_qty(price, qty, val, target) {
        val *= target;
        let newQty = val / price;
        newQty += 0.2;
        newQty = parseInt(newQty);
        // writeToEventLog(`Our new target quantity is ${newQty}`);
        return newQty - qty;
    }

    // Placing our orders
    async order_target(asset, target, qty) {
        if (target !== 0 && qty !== 0) {
        let side = "buy";
        if (qty < 0) side = "sell";
        qty = Math.abs(qty);
        // writeToEventLog(`Trying to ${side} ${qty} shares of ${asset}`);
        await this.submitMarketOrder(asset, qty, side);
        } else writeToEventLog(`Sufficiently leveraged in ${asset}`);
        writeToEventLog(`Let's get ${target} of our portfolio holding ${asset}`);
    }

    // Submit a market order if quantity is above 0.
    async submitMarketOrder(stock, quantity, side) {
        let errors = false;
        if (quantity > 0) {
        let resp = await this.alpaca
            .createOrder({
            symbol: stock,
            qty: quantity,
            side: side,
            type: "market",
            time_in_force: "day",
            })
            .catch((err) => {
            writeToEventLog(
                "Order of |" +
                quantity +
                " " +
                stock +
                " " +
                side +
                "| did not go through."
            );
            errors = true;
            writeToEventLog(err.message);
            });
        if (!errors) {
            this.updateChart()
        }
        } else {
        writeToEventLog(
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


    updateChart() {
        this.alpaca.getAccount().then((resp) => {
        this.chart.data.datasets[0].data.push({
            t: new Date(),
            y: resp.equity,
        });
        this.chart.update();
        });
        this.updatePositions();
        this.updateOrders();
    }


    updateOrders() {
        $("#orders-log").empty();
        this.alpaca
        .getOrders({
            status: "open",
        })
        .then((resp) => {
            resp.forEach((order) => {
            $("#orders-log").prepend(
                `<div class="order-inst">
                <p class="order-fragment">${order.symbol}</p>
                <p class="order-fragment">${order.qty}</p>
                <p class="order-fragment">${order.side}</p>
                <p class="order-fragment">${order.type}</p>
            </div>`
            );
            });
        });
    }


    // Log our positions
    async updatePositions() {
        $("#positions-log").empty();
        this.alpaca.getPositions().then((resp) => {
        resp.forEach((position) => {
            $("#positions-log").prepend(
            `<div class="position-inst">
                <p class="position-fragment">${position.symbol}</p>
                <p class="position-fragment">${position.qty}</p>
                <p class="position-fragment">${position.side}</p>
                <p class="position-fragment">${position.unrealized_pl}</p>
            </div>`
            );
        });
        });
    }
} // End of algo


// Run the algo class.
function runScript() {
  var API_KEY = $("#api-key").val();
  var API_SECRET = $("#api-secret").val();
  var F1 = new algo(API_KEY, API_SECRET);
  F1.run();
}
function killScript() {
  $("#event-log").html("Killing script.");
  F1.kill();
}
function writeToEventLog(text) {
  $("#event-log").prepend(`<p class="event-fragment">${text}</p>`);
}