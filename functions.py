import yfinance as yf
import json
import datetime
import random as rand

# Load dictionary binding stocks to their establishment date
with open("./data/stockdate.json") as infile:
   stockDate = json.load(infile)

# Generate initial date that ranges from 1970-1980
def getInitialDate():
    currentDate = datetime.date(1970 + round((rand.random() * 10)), round((rand.random() * 11)) + 1, round((rand.random() * 27)) + 1)
    return currentDate

# Retrieve price given a stock name as well as the date
def getPrice(stock, date):
    currentDateTime = datetime.datetime.fromordinal(date.toordinal())
    endDate = currentDateTime + datetime.timedelta(days=7)
    currentTicker = yf.Ticker(stock)
    hist = currentTicker.history(interval="1d", start=currentDateTime, end=endDate)
    currentPrice = format(round(hist['Close'].iloc[0], 2), '.2f')
    return currentPrice

# Retrieve information given a stock name
def getInfo(stock):
    currentTicker = yf.Ticker(stock)
    return currentTicker.info['longBusinessSummary'].replace("'", "")

# Generate a set of 3 random stocks given the date (to ensure each stock has been exists by the date)
def getOptions(date):
    options = []
    existingStocks = []
    for stock in stockDate:
        if datetime.datetime.strptime(stockDate[stock], '%Y-%m-%d').date() < date:
            existingStocks.append(stock)
    while len(options) < 3:
        potentialOption = existingStocks[rand.randrange(len(existingStocks))]
        try:
            currentPrice = getPrice(potentialOption, date)
            currentInfo = getInfo(potentialOption)
            options.append((potentialOption, len(options), currentPrice, currentInfo))
            stockDate.pop(potentialOption)
            existingStocks.pop(potentialOption)
        except:
            continue
    return options

# Push the graph to the left (for cases where none of ownedStocks 
# were bought before a certain date but those dates are still on the x-axis and in datesPast)
def pushLeft(ownedStocks, datesPast):
    while True:
        if ownedStocks:
            for stock in ownedStocks:
                if stock[2][0] != 'null':
                    keepGoing = False
                    break
                else:
                    keepGoing = True
            if keepGoing:
                for stock in ownedStocks:
                    stock[2].pop(0)
                datesPast.pop(0)
            else:
                break
        else:
            break