from flask import Flask
import pandas as pd
from alpha_vantage.timeseries import TimeSeries

app = Flask(__name__)
ticker = "TSLA"
keys = "LTR0QUJJTABLTQ11"

def factors(num):
  return [x for x in range (1, num+1) if num%x==0]

@app.route('/')
def home():
  return 0

@app.route('/getStackInfo')
def getStackInfo():
    time = TimeSeries(key = keys, output_format = 'pandas')
    data = time.get_daily(symbol=ticker, outputsize='full')
    return data

if __name__ == '__main__':
  app.run()