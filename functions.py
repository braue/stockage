import yfinance as yf
import json
import datetime
import random as rand

with open("./data/stockdate.json") as infile:
   stockDate = json.load(infile)

def getInitialDate():
    currentDate = datetime.date(1970 + round((rand.random() * 10)), round((rand.random() * 11)) + 1, round((rand.random() * 27)) + 1)
    return currentDate

def getPrice(stock, date):
    currentDateTime = datetime.datetime.fromordinal(date.toordinal())
    endDate = currentDateTime + datetime.timedelta(days=7)
    currentTicker = yf.Ticker(stock)
    hist = currentTicker.history(interval="1d", start=currentDateTime, end=endDate)
    currentPrice = format(round(hist['Close'].iloc[0], 2), '.2f')
    return currentPrice

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
            options.append((potentialOption, len(options), currentPrice))
            stockDate.pop(potentialOption)
        except:
            continue
    return options