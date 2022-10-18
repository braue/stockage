from flask import Flask, render_template, request
import yfinance as yf
import json
import datetime
import random as rand

with open("./data/stockdate.json") as infile:
   stockdate = json.load(infile)

currentDate = "doggy"
budget = 1000
existingStocks = []
ownedStocks = []

def startGame():

    currentDate = datetime.date(1970 + round((rand.random() * 10)), 1 + round((rand.random() * 11)), 1 + round((rand.random() * 27)))
    while currentDate.weekday() > 4:
        currentDate = currentDate.replace(day=round((rand.random() * 27)))

    for stock in stockdate:
        if datetime.datetime.strptime(stockdate[stock], '%Y-%m-%d').date() < currentDate:
            existingStocks.append(stock);

def stockPrompt():
    options = []
    for i in range(3):
        options.append(existingStocks[rand.randrange(len(existingStocks))])
    return options

app = Flask(__name__, template_folder='templates', static_folder='statics')

@app.route('/', methods=["GET", "POST"])
def game():
    data = [
        ("01-01-2020", 1597),
        ("02-01-2020", 1456),
        ("03-01-2020", 1908),
        ("04-01-2020", 896),
        ("05-01-2020", 755),
        ("06-01-2020", 453),
        ("07-01-2020", 3000),
        ("08-01-2020", 1293),
        ("09-01-2020", 1478),

    ]
    labels = [row[0] for row in data]
    values = [row[1] for row in data]

    if request.method == "GET":
        return render_template("main.html", labels=labels, values=values)