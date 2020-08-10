package main

import (
	"fmt"
	"log"
	"math"
	"os"

	"github.com/alpacahq/alpaca-trade-api-go/alpaca"
	"github.com/alpacahq/alpaca-trade-api-go/common"
	"github.com/joho/godotenv"
	"github.com/shopspring/decimal"
)

func goDotEnvVariable(key string) string {
	// load .env file
	err := godotenv.Load(".env")
	if err != nil {
		log.Fatalf("Error loading .env file")
	}
	return os.Getenv(key)
}

type alpacaClientContainer struct {
	client  *alpaca.Client
	stock   string
	weight  float64
	amtBars int
}

var alpacaClient alpacaClientContainer

func init() {
	os.Setenv(common.EnvApiKeyID, goDotEnvVariable("KEY"))
	os.Setenv(common.EnvApiSecretKey, goDotEnvVariable("SECRET"))

	// fmt.Printf("Running w/ credentials [%v %v]\n", common.Credentials().ID, common.Credentials().Secret)

	alpaca.SetBaseUrl(goDotEnvVariable("BASE_URL"))
	alpacaClient = alpacaClientContainer{
		alpaca.NewClient(common.Credentials()),
		"stock",
		0.0,
		10,
	}
}

func main() {
	acct, err := alpacaClient.client.GetAccount()
	if err != nil {
		panic(err)
	}

	i := 0
	for i < 5 {
		i++
		switch i {
		// Example portfolio weights
		case 1:
			alpacaClient.stock = "TLT" // Bonds ETF
			alpacaClient.weight = 0.20
		case 2:
			alpacaClient.stock = "GLD" // Gold ETF
			alpacaClient.weight = 0.10
		case 3:
			alpacaClient.stock = "QQQ" // NASDAQ ETF
			alpacaClient.weight = 0.20
		case 4:
			alpacaClient.stock = "DOW" // DOW ETF
			alpacaClient.weight = 0.20
		default:
			alpacaClient.stock = "SPY" // S&P 500 ETF
			alpacaClient.weight = 0.30
		}

		fmt.Printf("\nRebalancing our holdings in %s...\n\n", alpacaClient.stock)

		alpacaClient.run()
	}

	fmt.Println("\nFinished running Falcon One")
	acct, err = alpacaClient.client.GetAccount()
	if err != nil {
		panic(err)
	}
	fmt.Println("Portfolio's current value: ", acct.PortfolioValue)

	fmt.Println("Cash: ", acct.Cash)

}

// Run algorithm
func (alp alpacaClientContainer) run() {
	qty, holding := alp.getAssetQty()
	if holding {
		fmt.Printf("Holding %g shares of %s", qty, alp.stock)
		fmt.Println()
	} else {
		fmt.Println("We aren't holding any shares of ", alp.stock)
	}
	currentPrice := alp.getCurrPrice()
	fmt.Printf("%s's current price is %g", alp.stock, currentPrice)
	acct, _ := alp.client.GetAccount()
	portfolioValue, _ := acct.PortfolioValue.Float64()
	qty = alp.getQty(currentPrice, qty, portfolioValue)
	alp.submitMarketOrder(qty)
}

func (alp alpacaClientContainer) getAssetQty() (float64, bool) {
	position, err := alp.client.GetPosition(alpacaClient.stock)
	if err != nil {
		return 0.0, false
	}
	qty, _ := position.Qty.Float64()
	return qty, true
}

func (alp alpacaClientContainer) getCurrPrice() float64 {
	bars, _ := alp.client.GetSymbolBars(alpacaClient.stock, alpaca.ListBarParams{Timeframe: "minute", Limit: &alpacaClient.amtBars})
	currPrice := float64(bars[len(bars)-1].Close)
	return currPrice
}

func (alp alpacaClientContainer) getQty(price float64, qty float64, value float64) float64 {
	value *= alp.weight
	newQty := value / price
	newQty += 0.2
	fmt.Println("Our new target quantity is ", int(newQty))
	return float64((int(newQty) - int(qty)))
}

func (alp alpacaClientContainer) submitMarketOrder(qty float64) error {
	account, _ := alp.client.GetAccount()
	if int(qty) != 0 {
		side := "buy"
		if qty < 0 {
			side = "sell"
		}
		qty = math.Abs(qty)
		intQty := int(qty)
		fmt.Printf("Trying to %s %d shares of %s", side, intQty, alp.stock)

		adjSide := alpaca.Side(side)
		// PlaceOrder returns lastOrder object.. could use it to keep track of lastOrder.ID
		_, err := alp.client.PlaceOrder(alpaca.PlaceOrderRequest{
			AccountID:   account.ID,
			AssetKey:    &alp.stock,
			Qty:         decimal.NewFromFloat(float64(intQty)),
			Side:        adjSide,
			Type:        "market",
			TimeInForce: "day",
		})
		if err == nil {
			fmt.Printf("Market order of | %d %s %s | completed.\n", intQty, alp.stock, side)
			// alpacaClient.lastOrder = lastOrder.ID
		} else {
			fmt.Printf("Order of | %d %s %s | did not go through.\n", intQty, alp.stock, side)
		}
		return err
	}
	fmt.Printf("Quantity is <= 0, order of | %g %s | not sent.\n", qty, alp.stock)
	return nil
}
