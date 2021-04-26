from pymongo import MongoClient
from __init__ import parser # For reading mongodb Path from config file

class MongoDB:
    def __init__(self):
        mongoPath = parser.get('mongodb_config', 'mongopath')
        self.client = MongoClient(mongoPath)
        try:
            self.client = MongoClient(mongoPath)
        except Exception as e:
            print(e)
        self.stockDB = self.client.Stocks
        self.userDB = self.client.Users

    def getStockNames(self):
        return self.stockDB.list_collection_names()
