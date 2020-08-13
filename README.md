# Trading-Algorithms

This is a bunch of code that is me trying to learn the ins and outs of coding in Python. Specifically with API, CSV/TXT files, Redis Database and Pylivetrader. There is a little bit of me trying to migrate these algorithms into other programming languages as well. So far just Golang and JavaScript. The algorithms I have coded so far are simple rebalance algorithms.

## 📁 alpaca
Alpaca is an awesome trading platform for algorithmic trading. They have outstanding docs and an easy-to-work-with API. Here are some links to [Alpaca](https://app.alpaca.markets/login) and the [API docs](https://alpaca.markets/docs/)
### algo-data
* This script will give you some account information and data
* You need to instantiate some environment variables first
    * You can do this with export ENV_VAR="value"
    * Need your API Key, API Secret Key and API Base URL
* Run the script and get some insight into your account's performance

### get-acct-pct
* This is a possible addition to our WebApp
* This script is set up to be able to take in your API credentials as environment variables
* Then will find your true base value
* With that base value will calculate your total P/L of your account

### json-funct
* This is a script of several functions that will return json type
* Very useful if you are wanting to build your own algorithm within Alpaca
* There are many other functions that could be added to this script by reading the Alpaca Docs

### alpaca
* This is the original script that now just has leftover scraps that I didn't pull into a seperate script yet
* Still has some interesting things within but does need a clean-up
* Something specific that is cool in here is how to work with the Clock and whether the market is open/closed

### shortable-txt
* This script will read/write to and from txt files
* Checks whether a specific list of Assets is shortable and will do things accordingly
* Pretty great option for keeping track of when Assets are hard-to-borrow or not shortable
* However, I would recommend using the 'redis-shortable' script over this one
    * redis-shortable will not use other files and instead use the Redis database for quick speeds and less storage needed

## 📁 python
### algo.py
* This is a simple algorithm that incorporates daily rebalancing to limit volatility and increase returns 
    * Set up so you can edit your holdings and weights however you like
* Includes the schedule module which works brilliantly
* Allows for the algorithm to be ran 24/7 and only do things when you want to
* There is a Dockerfile in this directory that can help with running 24/7

### Dockerfile
* Built using conda but you could just as easily use a different python as long as it's python3
* Make sure to download each of your imports that aren't in the default library for python

### Running with Docker 24/7
```bash
# To run you can use to following command

$ docker pull 10.10.10.1:5000/algo-name \
&& docker run -d \
  --name algo_name \
  --restart unless-stopped \
  -e APCA_API_KEY_ID="some key ID" \
  -e APCA_API_SECRET_KEY="some secret KEY" \
  -e APCA_API_BASE_URL="https://api.alpaca.markets or https://paper-api.alpaca.markets" \
  10.10.10.1:5000/algo-name
```
### Build & Push Images
```bash
# To build and push you can use these commands (for portainer)

$ docker build --no-cache -t 10.10.10.1:5000/algo-name .
$ docker push 10.10.10.1:5000/algo-name
```
## 📁 js
### Falcon-Browser
* First need to download the folder from my github.. 
* Run the HTML file within a browser, I use Chrome. 
* Plug in your Alpaca Key ID and your Alpaca Secret Key ID
* Click on run and it will instantly run Falcon One Algorithm within your account
    * Must be a paper account unless you tweak some code.
* The script will output some logs as well as your positions open and the orders placed

### algo.js
* This is a simple algorithm that incorporates daily rebalancing to limit volatility and increase returns 
    * Set up so you can edit your holdings and weights however you like
* Environment Variable Setup
    * Create a .env file with your api credentials
        * APCA_API_KEY_ID=apiKey
        * APCA_API_SECRET_KEY=secretKey
        * APCA_API_BASE_URL=https://paper-api.alpaca.markets
    * Create a package.json file
        * 'npm init -y' in your terminal will do this for you, be sure to cd to the same directory as your .env file
    * Install the dotenv npm package
        * npm install dotenv

## 📁 go
### algo.go
* This is a simple algorithm that incorporates daily rebalancing to limit volatility and increase returns 
    * Set up so you can edit your holdings and weights however you like
* Environment Variable Setup
    * There are several ways to set and get environment variables with Go
    * I chose to use the GoDotEnv Package
        1. Install the GoDotEnv Package - $ go get github.com/joho/godotenv
        2. Create the .env file within the same directory as your algorithm
* Download Alpaca Packages
    * $ go get github.com/alpacahq/alpaca-trade-api-go/common
    * $ go get github.com/alpacahq/alpaca-trade-api-go/polygon
    * $ go get github.com/alpacahq/alpaca-trade-api-go/stream
    * $ go get github.com/alpacahq/alpaca-trade-api-go/alpaca
* Download Decimal Package
    * $ go get github.com/shopspring/decimal

## 📁 demo-redis
[redis](https://redis.io/)
```
This is a very limited example of the possible uses of Redis Database. There are several different clients for most languages. I have 2 Golang client examples. I prefer redigo over redis-go since it has a similar simplistic feel to the redis in python.
```
### Go 📁
**redigo**
* [Install Directions](https://github.com/gomodule/redigo#installation)
* [Go Connection Examples](https://docs.objectrocket.com/redis_go_examples.html)
**go-redis**
* [Install Directions](https://github.com/go-redis/redis#installation)
* [GoDocs](https://pkg.go.dev/github.com/go-redis/redis/v8?tab=doc#pkg-examples)

### JavaScript
**ioredis**
* [Install Directions](https://github.com/luin/ioredis#install)
* [Other Examples](https://github.com/luin/ioredis/tree/master/examples)

### Python
**redis**
* Check my other repo [twitter-bot](https://github.com/abspen1/twitter-bot#prerequisites) for redis install directions
* I also implement redis in several ways in that repo so a great resource for more examples
* In my [Fantasy-Twitter](https://github.com/abspen1/Fantasy-Twitter/blob/master/main.py) script I also use Redis.
* In my opinion, Redis is the easiest to manipulate in Python. Could be biased since I've used Redis with Python the most out of the three

## 📁 redis-shortable
### main.py
* This script uses Redis database to keep track of how frequently specific Assets are actually shortable
* Good to know if you're wanting to short Assets that frequently fluctuate from hard-to-borrow or to un-shortable
* I created this script to keep track of how frequently Volatility ETF's are shortable
* There is a Dockerfile as well that will allow you to run this script each morning automatically

### Redis Setup
* Download redis and activate your redis server, a simple youtube search will do
* Start running your redis-server
* Next open your redis-cli
  * Be sure to change the requirepass within your config to secure your server
  * Within redis-cli// > config get requirepass
    1. "requirepass"
    2. "This Will Be Empty"
* Set your password
  * Within redis-cli// > config set requirepass yourPasswordHere (recommended at least 32 characters long)

### Running
```bash
# To run redis-shortable use the following docker command

docker pull 10.10.10.1:5000/algo-name \
&& docker run -d \
  --name algo_name \
  --restart unless-stopped \
  -e APCA_API_KEY_ID="some key ID" \
  -e APCA_API_SECRET_KEY="some secret KEY" \
  -e APCA_API_BASE_URL="https://api.alpaca.markets or https://paper-api.alpaca.markets" \
  10.10.10.1:5000/algo-name
```

### Build and push image
```bash
# To build and push you can use these commands (for portainer)

$ docker build --no-cache -t 10.10.10.1:5000/algo-name .
$ docker push 10.10.10.1:5000/algo-name
```

## Some to-do's with my scripts here
**Migrate to other languages**
* Figure out how to run the JavaScript and Go algorithms in docker 24/7
* Clean up the code
* Write a more complex trading algorithm
**go**
* Try to get a web browser trader with the Go program as backend
**python**
* Try to get a web browser trader with Python as backend
