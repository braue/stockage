from flask import Flask, render_template, request, redirect, session
import yfinance as yf
import json
import datetime
import random as rand
from functions import getInitialDate, getPrice, getOptions, pushLeft

# Example data to present in the background of the start game screen
with open("./data/example.json") as infile:
    exampleData = json.load(infile)
exampleLabels = [row[0] for row in exampleData]
exampleValues = [row[1] for row in exampleData]
exampleDate = ['08 March 1977', '03/08/1977']
exampleBudget = 178.94
exampleOptions = [('NEE', 0, '1.45', 'Example'), ('GT', 1, '0.28', 'Example'), ('QRB', 2, '6.22', 'Example')]
exampleFinish = [False, None]

# Initialize flask app
app = Flask(__name__, template_folder='templates', static_folder='statics')
app.secret_key = "SUPA_SECRET"

# Main page that presents all the data
@app.route('/', methods=["GET"])
def main():
    #Until activeGame is set to true (clicking start game) the page will return the start game screen
    if 'activeGame' in session and session['activeGame']:
        return render_template("main.html", activeGame=session['activeGame'], currentDate=session['currentDate'], budget=session['budget'], options=session['options'], ownedStocks=session['ownedStocks'], datesPast=session['datesPast'], finished=session['finished'], error=session['error'])
    else:
        session['activeGame'] = False
        return render_template("main.html", activeGame=session['activeGame'], currentDate=exampleDate, budget=exampleBudget, options=exampleOptions, finished=exampleFinish, error=[], exampleValues=exampleValues, exampleLabels=exampleLabels)

# Page sets initial session variables and activates game when start game is clicked
@app.route('/startGame', methods=["POST"])
def startGame():
    currentDate = getInitialDate()
    session['currentDate'] = [currentDate.strftime('%d %B %Y'), currentDate.strftime('%m/%d/%Y') ]
    session['options'] = getOptions(currentDate)
    session['budget'] = format(1000.00, '.2f')
    session['ownedStocks'] = []
    session['datesPast'] = []
    session['activeGame'] = True
    session['finished'] = [False, None]
    session['error'] = []
    return redirect('/')

# Page processes incrementing the date as well as buying stocks when increment is clicked
@app.route('/increment', methods=["POST"])
def increment():
    # Reset error
    session['error'] = []
    # Stock math and check if the money invested exceeds budget (error if so)
    currentPrices = []
    amntsShares = []
    investments = []
    paidList = []
    for input in ['0', '1', '2']:
        investment = float(request.form[input]) if request.form[input] else 0
        investments.append(investment)
        currentPrice = float(session['options'][int(input)][2])
        currentPrices.append(currentPrice)
        amntShares = investment // currentPrice
        amntsShares.append(amntShares)
        pricePaid = amntShares * currentPrice
        paidList.append(pricePaid)
    if sum(investments) > float(session['budget']):
        session['error'].append("You dont have that much money")
        return redirect('/')
    # Append currentDate to datesPast
    session['datesPast'].append(session['currentDate'][1])
    # Append stocks purchased to ownedStocks
    for input in ['0', '1', '2']:
        session['budget'] = format(float(session['budget']) - paidList[int(input)], '.2f')
        if amntsShares[int(input)] >= 1:
            priceList = ['null' for i in range(len(session['datesPast']) - 1)]
            priceList.append(currentPrices[int(input)])
            graphColor = "rgb({red}, {green}, {blue})".format(red=round(rand.random() * 255),green=round(rand.random() * 255),blue=round(rand.random() * 255))
            session['ownedStocks'].append([session['options'][int(input)][0], int(amntsShares[int(input)]), priceList, len(session['ownedStocks']), graphColor])
    # Increment currentDate and check if the new date exceeds current (real) date (finish if so)
    currentDate = datetime.datetime.strptime(session['currentDate'][0], '%d %B %Y')
    currentDate = currentDate.replace(day=(round(rand.random() * 27) + 1), month=(round((rand.random() * 11)) + 1), year=(currentDate.year + round(rand.random() * 2) + 4))
    if currentDate >= datetime.datetime.today():
        session['finished'][0] = True
        for i in range(len(session['ownedStocks'])-1, -1, -1):
            session['budget'] = format(float(session['budget']) + session['ownedStocks'][i][1] * session['ownedStocks'][i][2][-1], '.2f')
            session['ownedStocks'].pop(i)
        session['finished'][1] = float(session['budget']) >= 100000.00
        return redirect('/')
    session['currentDate'][0] = currentDate.strftime('%d %B %Y')
    session['currentDate'][1] = currentDate.strftime('%m/%d/%Y')
    # Append new prices to ownedStocks (for new currentDate)
    for stock in session['ownedStocks']:
        try:
            currentPrice = getPrice(stock[0], currentDate.date())
            stock[2].append(float(currentPrice))
        except:
            stock[2].append('null')
    # Get new options
    session['options'] = getOptions(currentDate.date())
    # Push the stock graph to the left
    pushLeft(session['ownedStocks'], session['datesPast'])
    return redirect('/')

# Page processes the sale of a stock when sell is clicked
@app.route('/sell', methods=["POST"])
def sell():
    # Reset error
    session['error'] = []
    # Add to budget
    session['budget'] = format(float(session['budget']) + session['ownedStocks'][int(request.form['sell'])][1] * session['ownedStocks'][int(request.form['sell'])][2][-1], '.2f')
    # Remove from ownedStocks
    session['ownedStocks'].pop(int(request.form['sell']))
    # Standardize indexes
    for idx, stock in enumerate(session['ownedStocks']):
        stock[3] = idx
    # Push the stock graph to the left
    pushLeft(session['ownedStocks'], session['datesPast'])
    return redirect('/')

# Page processes the end of the game when end game is clicked
@app.route('/endGame', methods=["POST"])
def endGame():
    session['activeGame'] = False
    return redirect('/')