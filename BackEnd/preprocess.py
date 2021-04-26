import pymongo
from datetime import datetime
from time import sleep
from pandas import Timestamp
import pandas as pd
from mongoDB import MongoDB

class StockData:

    def __init__(self):
        self.clientObj = MongoDB()
        self.clientDB = self.clientObj.stockDB

    def getExtendedTimeSeries(self, symbol, interval, stockSlice, adjusted, apiKey):
        #'https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY_EXTENDED&symbol=IBM&interval=60min&slice=year1month3&adjusted=false&apikey=demo'

        api='https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY_EXTENDED&symbol='+symbol+'&interval='+interval+'&slice='+stockSlice+'&adjusted='+adjusted+'&apikey='+apiKey
        
        if api is None:
            return None

        data = pd.read_csv(api)
        data['time'] = data['time'].apply( lambda x: datetime.strptime(x, "%Y-%m-%d %H:%M:%S"))

        return data.to_dict("records")

    # To create stock collection data(5min interval) for any company for last 2 years
    def createStockData(self, ticker, interval = '5min', adjusted = 'false', limit=24, apiKey='LTR0QUJJTABLTQ11'):
        collection = self.clientDB[ticker]
        yearNum = 1
        monthNum = 1
        for i in range(limit):
            if monthNum > 12:
                yearNum += 1
                monthNum = 1
                sleep(30)
            # To handle 5 api calls to Alpha Vantage per minute
            if monthNum%5 == 0:
                print("Sleeping for 45 secs")
                sleep(45)

            stockSlice='year'+str(yearNum)+'month'+str(monthNum)
            data = self.getExtendedTimeSeries(ticker, interval, stockSlice, adjusted, apiKey)
            if data is None:
                print("No data available from alpha vantage API")
                return

            collection.insert_many(data)
            print(monthNum," Done")
            monthNum += 1
        print("Insertion Done")
        sleep(30)

    # To Delete any company's stock data from DB
    def deleteStockData(self, ticker):
        collection = self.clientDB[ticker]
        collection.drop()
        print("Collection Droped")


if __name__ =='__main__':
 
    tickers = ['MSFT', 'AAPL']
    a = StockData()
    for ticker in tickers:
        print(ticker)
        a.createStockData(ticker)