import yfinance as yf
import json
import datetime
import random as rand

with open("./data/stockdate.json") as infile:
    stockdate = json.load(infile)

currentDate = None
budget = 1000
existingStocks = []
ownedStocks = []

def startGame():

    currentdate = datetime.date(1970 + round((rand.random() * 10)), 1 + round((rand.random() * 11)), 1 + round((rand.random() * 27)))
    while currentdate.weekday() > 4:
        currentdate = currentdate.replace(day=round((rand.random() * 27)))

    for stock in stockdate:
        if datetime.datetime.strptime(stockdate[stock], '%Y-%m-%d').date() < currentdate:
            existingStocks.append(stock);

def stockPrompt():
    options = []
    for i in range(3):
        options.append(existingStocks[rand.randrange(len(existingStocks))])
    return options

startGame()
print(stockPrompt())