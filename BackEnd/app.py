from flask import Flask
from flask import request, jsonify
import pymongo
from mongoDB import MongoDB
import pandas as pd
from datetime import datetime

app = Flask(__name__)

@app.route('/')
# Home Page
def startPage():
    pass

@app.route('/getStockData', methods=['GET','POST'])
# Get stock data to create graph
def getStockData():
    req = request.get_json()
    ticker = req.get('ticker')
    # ticker = 'TSLA'
    if req.get('duration') is None:
        duration = 'year'
    else:
        duration = req.get('duration')

    database = getStockDB()
    collection = database[ticker]
    end = getLastDate(collection)
    start = getStartDate(collection, duration, end)

    df = pd.DataFrame(collection.find({'time':{'$gte':end, '$lt':start}},{'_id':0}))
    return df.to_json()

# Get stock database object
def getStockDB():
    client = MongoDB()
    return client.stockDB

# Get last date entry in ticker collection
def getLastDate(collection):
    return collection.find().sort({'time': -1},{'time':1}).limit(1)

# Get start date entry in ticker collection according to duration
def getStartDate(collection, duration, end):
    if duration == 'max':
        start = collection.find().sort({'time': 1},{'time':1}).limit(1)
    elif duration == 'year':
        start = end.AddYears(-1)
    elif duration == 'month':
        start = end.AddMonths(-1)
    elif duration == 'day':
        start = end.AddDays(-1)
    elif duration == 'hour':
        start = end.AddHoues(-1)
    return start


app.run(host="0.0.0.0", port="9990")
    