import json
import pandas_datareader as web
from datetime import datetime
import unicodedata
import os
import requests


STOCKS_URL = 'https://api.iextrading.com/1.0/ref-data/symbols'
CHANNEL = 'iex'

STOCKS_FOLDER = 'files/stocks'
STOCK_NAMES_FILE = 'stock_names.json'

DATE_FROM = datetime(2017, 1, 1)
DATE_TO = datetime(2019, 12, 22)

FOLDER = os.path.dirname(os.path.abspath(__file__)) + '/' + STOCKS_FOLDER + '/'


def to_string(u_string):
    return unicodedata.normalize('NFKD', u_string).encode('ascii', 'ignore')


def save_stocks(skip_exists):
    folder = os.path.dirname(os.path.abspath(__file__)) + '/' + STOCKS_FOLDER + '/'
    stock_names_file_path = folder + STOCK_NAMES_FILE

    # Get stock names
    if os.path.isfile(stock_names_file_path):
        with open(stock_names_file_path) as stock_names_file:
            stock_names = json.load(stock_names_file)
    else:
        response = requests.get(STOCKS_URL)
        stock_names_json = response.content
        stock_names_file = open(folder + STOCK_NAMES_FILE, "w")
        stock_names_file.write(stock_names_json)
        stock_names_file.close()
        stock_names = json.loads(stock_names_json)

    data = stock_names
    count_stoks = len(data)
    print count_stoks

    for stock in data:
        symbol = to_string(stock['symbol'])
        name = to_string(stock['name'])
        file_path = folder + symbol + '.csv'

        if skip_exists and os.path.isfile(file_path):
            print 'file for ' + name + ' already exists'
            continue

        stock_data = web.DataReader(symbol, CHANNEL, DATE_FROM, DATE_TO)
        stock_data.to_csv(file_path)
        print name + ' was saved'


# save_stocks(True)
