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
    currentDate = datetime.date(1970 + round((rand.random() * 10)), 1 + round((rand.random() * 11)), 1 + round((rand.random() * 27)))
    while currentDate.weekday() > 4:
        currentDate = currentDate.replace(day=round((rand.random() * 27)))
    return currentDate

def getOptions(date):
    options = []
    existingStocks = []
    for stock in stockDate:
        if datetime.datetime.strptime(stockDate[stock], '%Y-%m-%d').date() < date:
            existingStocks.append(stock)
    for i in range(3):
        options.append(existingStocks[rand.randrange(len(existingStocks))])
    return options

app = Flask(__name__, template_folder='templates', static_folder='statics')
app.secret_key = "SUPA_SECRET"

@app.route('/', methods=["GET"])
def main():
    try:
        return render_template("main.html", activeGame=session['activeGame'], currentDate=session['currentDate'], budget=session['budget'], options=session['options'], exampleValues=exampleValues, exampleLabels=exampleLabels)
    except KeyError:
        session['activeGame'] = False
        return render_template("main.html", activeGame=session['activeGame'], exampleValues=exampleValues, exampleLabels=exampleLabels)

@app.route('/startGame', methods=["POST"])
def startGame():
    currentDate = getInitialDate()
    session['currentDate'] = currentDate.strftime('%d %B %Y')
    session['options'] = getOptions(currentDate)
    session['budget'] = 1000
    session['ownedStocks'] = []
    session['activeGame'] = True
    return redirect('/')