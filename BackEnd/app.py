from flask import Flask
from flask import request, jsonify;
import pymongo;

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/getStockData', methods=['GET','POST'])
def getStockData():
    req = request.get_json();
    ticker = req.get('ticker');
    start = req.get('start');
    end = req.get('end');
    interval = req.get('interval');

    mongoClient = getDBConnection();

    database = "Stocks";
    db = mongoClient[database];
    collection = db[ticker];
    print(ticker);
    json = collection.find_one({},{"_id":0});
    print(json);
    return jsonify(json);

def getDBConnection():
    client = None;
    try:
        client = pymongo.MongoClient("mongodb+srv://dbAdmin:Safetrade@cluster0.rpnkw.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
    except Exception as e:
        print(e);

    return client;

app.run()
    