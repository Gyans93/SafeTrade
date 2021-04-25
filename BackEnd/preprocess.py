import pymongo
import datetime
from pandas import Timestamp
import pandas as pd


def getExtendedTimeSeries(symbol, interval, stockSlice, adjusted, apiKey):
    #'https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY_EXTENDED&symbol=IBM&interval=60min&slice=year1month3&adjusted=false&apikey=demo'

    api='https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY_EXTENDED&symbol='+symbol+'&interval='+interval+'&slice='+stockSlice+'&adjusted='+adjusted+'&apikey='+apiKey

    data = pd.read_csv(api)
    data['time'] = data['time'].apply( lambda x: datetime.datetime.strptime(x, "%Y-%m-%d %H:%M:%S"))

    return data.to_dict("records")

def updateStockData(ticker, interval = '5min', adjusted = 'false', limit=24, apiKey='LTR0QUJJTABLTQ11'):

    limit+=1
    month=1
    for i in range(1,limit):
        if(i==13):
            month+=1
            i=i%12

    stockSlice='year'+str(month)+'month'+str(i)
    data = getExtendedTimeSeries(ticker, interval, stockSlice, adjusted, apiKey)
    


if __name__ =='__main__':

    ticker = 'TSLA'
    sdf = getExtendedTimeSeries(ticker, '5min', 'year1month12','false')
    client = pymongo.MongoClient("mongodb+srv://dbAdmin:Safetrade@cluster0.rpnkw.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
    db = client.Stocks

    collection = db[ticker]
    collection.insert_many(sdf)