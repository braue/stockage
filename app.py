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
    while currentDate.weekday() > 4:
        currentDate = currentDate.replace(day=round((rand.random() * 27)))
    return currentDate

def getOptions(date):
    options = []
    existingStocks = []
    currentDateTime = datetime.datetime.fromordinal(date.toordinal())
    endDate = currentDateTime + datetime.timedelta(days=1)
    for stock in stockDate:
        if datetime.datetime.strptime(stockDate[stock], '%Y-%m-%d').date() < date:
            existingStocks.append(stock)
    for i in range(3):
        options.append(existingStocks[rand.randrange(len(existingStocks))])
    for idx, option in enumerate(options):
        currentTicker = yf.Ticker(option)
        hist = currentTicker.history(interval="1d", start=currentDateTime, end=endDate)
        currentPrice = format(round(hist['Close'].iloc[0], 2), '.2f')
        options[idx] = (option, idx, currentPrice)
    return options

app = Flask(__name__, template_folder='templates', static_folder='statics')
app.secret_key = "SUPA_SECRET"

@app.route('/', methods=["GET"])
def main():

    #Main app interface
    if 'activeGame' in session and session['activeGame']:
        return render_template("main.html", activeGame=session['activeGame'], currentDate=session['currentDate'], budget=session['budget'], options=session['options'])
    else:
        session['activeGame'] = False
        return render_template("main.html", activeGame=session['activeGame'], exampleValues=exampleValues, exampleLabels=exampleLabels)

@app.route('/startGame', methods=["POST"])
def startGame():
    
    #Initialize session values
    currentDate = getInitialDate()
    session['currentDate'] = currentDate.strftime('%d %B %Y')
    session['options'] = getOptions(currentDate)
    session['budget'] = format(1000.00, '.2f')
    session['ownedStocks'] = []
    session['activeGame'] = True
    return redirect('/')

@app.route('/increment', methods=["POST"])
def increment():

    #Increment currentDate (2-5 years)
    currentDate = datetime.datetime.strptime(session['currentDate'], '%d %B %Y')
    currentDate = currentDate.replace(day=(round((rand.random() * 27)) + 1), month=(round((rand.random() * 11)) + 1), year=(currentDate.year + round(rand.random() * 3) + 2))
    while currentDate.weekday() > 4:
        currentDate = currentDate.replace(day=round((rand.random() * 27)))
    session['currentDate'] = currentDate.strftime('%d %B %Y')

    #Add bought stocks to ownedStocks
    #Get current price and floor divide request.form by that price to get resulting amount of shares
    #Modulo it to give remainder (put back into budget)
    #Subtract from budget the floor divided number multipled by the price of stock
    for input in ['0', '1', '2']:
        if request.form[input] == '':
           request.form[input] = '0'
        amntShares = session['options'][int(input)][-1] // request.form[input]
        pricePaid = amntShares * session['options'][int(input)]
        session['budget'] -= pricePaid
        #session['ownedStocks'].append()

        
    

    #MUST UPDATE CURRENTDATE, OPTIONS, BUDGET, OWNEDSTOCKS
    return redirect('/')