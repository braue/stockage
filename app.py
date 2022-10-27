from flask import Flask, render_template, request, redirect, url_for, session
import yfinance as yf
import json
import datetime
import random as rand
from functions import getInitialDate, getPrice, getOptions

with open("./data/example.json") as infile:
    exampleData = json.load(infile)

exampleLabels = [row[0] for row in exampleData]
exampleValues = [row[1] for row in exampleData]

app = Flask(__name__, template_folder='templates', static_folder='statics')
app.secret_key = "SUPA_SECRET"

@app.route('/', methods=["GET"])
def main():

    if 'activeGame' in session and session['activeGame']:
        return render_template("main.html", activeGame=session['activeGame'], currentDate=session['currentDate'], budget=session['budget'], options=session['options'], ownedStocks=session['ownedStocks'], datesPast=session['datesPast'], finished=session['finished'])
    else:
        session['activeGame'] = False
        session['finished'] = [False, None]
        return render_template("main.html", activeGame=session['activeGame'], finished=session['finished'], exampleValues=exampleValues, exampleLabels=exampleLabels)

@app.route('/startGame', methods=["POST"])
def startGame():
    
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

    currentPrices = []
    amntsShares = []
    paidList = []
    for input in ['0', '1', '2']:
        investment = float(request.form[input]) if request.form[input] else 0
        currentPrice = float(session['options'][int(input)][2])
        currentPrices.append(currentPrice)
        amntShares = investment // currentPrice
        amntsShares.append(amntShares)
        pricePaid = amntShares * currentPrice
        paidList.append(pricePaid)
    if sum(paidList) > float(session['budget']):
        return redirect('/')
    
    session['datesPast'].append(session['currentDate'][1])

    for input in ['0', '1', '2']:
        session['budget'] = format(float(session['budget']) - paidList[int(input)], '.2f')
        if amntsShares[int(input)] >= 1:
            priceList = ['null' for i in range(len(session['datesPast']) - 1)]
            priceList.append(currentPrices[int(input)])
            graphColor = "rgb({red}, {green}, {blue})".format(red=round(rand.random() * 255),green=round(rand.random() * 255),blue=round(rand.random() * 255))
            session['ownedStocks'].append([session['options'][int(input)][0], int(amntsShares[int(input)]), priceList, len(session['ownedStocks']), graphColor])

    currentDate = datetime.datetime.strptime(session['currentDate'][0], '%d %B %Y')
    currentDate = currentDate.replace(day=(round(rand.random() * 27) + 1), month=(round((rand.random() * 11)) + 1), year=(currentDate.year + round(rand.random() * 3) + 2))
    if currentDate >= datetime.datetime.today():
        session['finished'][0] = True
        print(session['ownedStocks'])
        print("len = " + str(len(session['ownedStocks'])))
        for i in range(len(session['ownedStocks'])-1, -1, -1):
            print('running index: ' + str(i))
            session['budget'] = format(float(session['budget']) + session['ownedStocks'][i][1] * session['ownedStocks'][i][2][-1], '.2f')
            session['ownedStocks'].pop(i)
        session['finished'][1] = float(session['budget']) >= 100000.00
        return redirect('/')
    session['currentDate'][0] = currentDate.strftime('%d %B %Y')
    session['currentDate'][1] = currentDate.strftime('%m/%d/%Y')

    for stock in session['ownedStocks']:
        try:
            currentPrice = getPrice(stock[0], currentDate.date())
            stock[2].append(float(currentPrice))
        except:
            stock[2].append('null')

    session['options'] = getOptions(currentDate.date())

    return redirect('/')

@app.route('/sell', methods=["POST"])
def sell():
    print(session['ownedStocks'])
    print(request.form['sell'])
    session['budget'] = format(float(session['budget']) + session['ownedStocks'][int(request.form['sell'])][1] * session['ownedStocks'][int(request.form['sell'])][2][-1], '.2f')
    session['ownedStocks'].pop(int(request.form['sell']))
    for idx, stock in enumerate(session['ownedStocks']):
        stock[3] = idx
    print(session['ownedStocks'])
    print(request.form['sell'])
    return redirect('/')

@app.route('/endGame', methods=["POST"])
def endGame():
    session['activeGame'] = False
    return redirect('/')