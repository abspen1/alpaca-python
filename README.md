# Trading-Algorithms
```bash
This is a bunch of code that is me trying to learn the ins and outs of coding. Specifically with API, CSV/TXT files, Redis Database and Pylivetrader. There is a little bit of me trying to migrate these algorithms into other programming languages as well. So far just Golang and JavaScript. The algorithms I have coded so far are simple rebalance algorithms.
```

## Main
**algo-data**
* This script will give you some account information and data
* You need to instantiate some environment variables first
    * You can do this with export ENV_VAR="value"
    * Need your API Key, API Secret Key and API Base URL
* Run the script and get some insight into your account's performance

**demo-redis**
* This is bunch of commented out code that I've used when hard coding some variables into Redis and just learning how to use Redis
* There's example for how to do many things in Redis with Python in this script
* Uncomment out items to see how they would work within your Redis Server
    * See below for how to set up your own Redis Server
* Need the Redis password passed as an environment variable

**get-acct-pct**
* This is a possible addition to our WebApp
* This script is set up to be able to take in your API credentials as environment variables
* Then will find your true base value
* With that base value will calculate your total P/L of your account

**json-funct**
* This is a script of several functions that will return json type
* Very useful if you are wanting to build your own algorithm within Alpaca
* There are many other functions that could be added to this script by reading the Alpaca Docs

**main**
* This is the original script that now just has leftover scraps that I didn't pull into a seperate script yet
* Still has some interesting things within but does need a clean-up
* Something specific that is cool in here is how to work with the Clock and whether the market is open/closed

**shortable-txt**
* This script will read/write to and from txt files
* Checks whether a specific list of Assets is shortable and will do things accordingly
* Pretty great option for keeping track of when Assets are hard-to-borrow or not shortable
* However, I would recommend using the 'redis-shortable' script over this one
    * redis-shortable will not use other files and instead use the Redis database for quick speeds and less storage needed


## js-algo
**Falcon-Broswer**
* First Need to download the folder from my github.. 
* Run the HTML file within a browser, I use Chrome. 
* Plug in your Alpaca Key ID and your Alpaca Secret Key ID
* Click on run and it will instantly run Falcon One Algorithm within your account
    * Must be a paper account unless you tweak some code.
* The script will output some logs as well as your positions open and the orders placed

**long-short-browser**
* This is an example I used from the alpaca JS github
* I used this example to help me with the Falcon-Browser 
* I need to take a longer class on HTML and CSS as I'm still uncomfortable using

**algo.js**
* Environment Variable Setup
    * Create a .env file with your api credentials
        * APCA_API_KEY_ID=apiKey
        * APCA_API_SECRET_KEY=secretKey
        * APCA_API_BASE_URL=https://paper-api.alpaca.markets
    * Create a package.json file
        * 'npm init -y' in your terminal will do this for you
    * Install the dotenv npm package
        * npm install dotenv
* This is a simple algorithm that incorporates daily rebalancing to limit volatility and increase returns using leveraged ETF's
    * Set up so you can edit your holdings and weights however you like


## redis-shortable
* This script uses Redis database to keep track of how frequently specific Assets are actually shortable
* Good to know if you're wanting to short Assets that frequently fluctuate from hard-to-borrow or to un-shortable
* I created this script to keep track of how frequently Volatility ETF's are shortable
* There is a Dockerfile as well that will allow you to run this script each morning automatically


## Some to-do's with my scripts here
**Migrate to other languages**
* Figure out how to run the JavaScript and Go algorithms in docker 24/7
* Clean up the code
* Write a more complex trading algorithm