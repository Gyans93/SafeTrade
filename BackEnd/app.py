from flask import Flask
from flask import request, jsonify
import pymongo
from mongoDB import MongoDB
import pandas as pd

app = Flask(__name__)

@app.route('/')
def startPage():
    pass

@app.route('/getStockData', methods=['GET','POST'])
def getStockData():
    req = request.get_json()
    ticker = req.get('ticker')
    # ticker = 'TSLA'
    start = req.get('start')
    end = req.get('end')
    interval = req.get('interval')

    database = getDB()
    collection = database[ticker]
    print(ticker)
    df = pd.DataFrame(collection.find({'time':{'$gte':end, '$lt':start}},{'_id':0}).limit(5))
    return df.to_json()

def getDB():
    client = MongoDB()
    return client.db

app.run(host="0.0.0.0", port="9990")
    