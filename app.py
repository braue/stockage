from flask import Flask, render_template, request, redirect, url_for, session
import yfinance as yf
import json
import datetime
import random as rand

with open("./data/stockdate.json") as infile:
   stockDate = json.load(infile)

with open("./data/example.json") as infile:
    exampleData = json.load(infile)

exampleLabels = [row[0] for row in exampleData]
exampleValues = [row[1] for row in exampleData]

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
    for i in range(3):
        options.append(existingStocks[rand.randrange(len(existingStocks))])
    for idx, option in enumerate(options):
        currentPrice = getPrice(option, date)
        options[idx] = (option, idx, currentPrice)
    return options

app = Flask(__name__, template_folder='templates', static_folder='statics')
app.secret_key = "SUPA_SECRET"

@app.route('/', methods=["GET"])
def main():

    #Main app interface
    if 'activeGame' in session and session['activeGame']:
        return render_template("main.html", activeGame=session['activeGame'], currentDate=session['currentDate'], budget=session['budget'], options=session['options'], ownedStocks=session['ownedStocks'], datesPast=session['datesPast'])
    else:
        session['activeGame'] = False
        return render_template("main.html", activeGame=session['activeGame'], exampleValues=exampleValues, exampleLabels=exampleLabels)

@app.route('/startGame', methods=["POST"])
def startGame():
    
    #Initialize session values
    currentDate = getInitialDate()
    session['currentDate'] = [currentDate.strftime('%d %B %Y'), currentDate.strftime('%m/%d/%Y') ]
    session['options'] = getOptions(currentDate)
    session['budget'] = format(1000.00, '.2f')
    session['ownedStocks'] = []
    session['datesPast'] = []
    session['activeGame'] = True
    return redirect('/')

@app.route('/increment', methods=["POST"])
def increment():

    session['datesPast'].append(session['currentDate'][1])

    for input in ['0', '1', '2']:
        investment = float(request.form[input]) if request.form[input] else 0
        currentPrice = float(session['options'][int(input)][-1])
        amntShares = investment // currentPrice
        pricePaid = amntShares * currentPrice
        session['budget'] = format(float(session['budget']) - pricePaid, '.2f')
        if amntShares >= 1:
            priceList = ['null' for i in range(len(session['datesPast']) - 1)]
            priceList.append(currentPrice)
            session['ownedStocks'].append([session['options'][int(input)][0], int(amntShares), priceList])

    #Increment currentDate (2-5 years)

    currentDate = datetime.datetime.strptime(session['currentDate'][0], '%d %B %Y')
    currentDate = currentDate.replace(day=(round((rand.random() * 27)) + 1), month=(round((rand.random() * 11)) + 1), year=(currentDate.year + round(rand.random() * 3) + 2))
    session['currentDate'][0] = currentDate.strftime('%d %B %Y')
    session['currentDate'][1] = currentDate.strftime('%m/%d/%Y')

    #Add new prices to ownedStocks

    for stock in session['ownedStocks']:
        currentPrice = getPrice(stock[0], currentDate.date())
        stock[2].append(float(currentPrice))

    #Update options
    session['options'] = getOptions(currentDate.date())

    return redirect('/')