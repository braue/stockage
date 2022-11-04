# stockpile

## what
Stockpile is a stock trading game that utilizes historical stock data to allow you to simulate an investment journey spanning the 70s/80s to the current day.

## how
- Flask: connects Python with HTML.
- yfinance: retrieves the historical stock price and description data.
- Chart.js: displays the graph of the stock prices.

## why
I find the concept of simulating investments in the past, especially with the hindsight we have today, to be fascinating. Getting lucky in the early game spotting a $0.05 Walmart or Nike stock is super exciting.

## improvements
- At the moment, API calls to yfinance are made on every increment. This leads to extremely slow load times. This problem can be resolved by pre-loading all of the dates and stock data. This might slightly increase the initial load time after starting a game, but the rest will be completely smooth.
