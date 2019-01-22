import pandas as pd
from settings import *
import json
import unicodedata


def to_string(u_string):
    if not isinstance(u_string, unicode):
        return u_string
    return unicodedata.normalize('NFKD', u_string).encode('ascii', 'ignore')


def delete_symbol(symbol):
    if os.path.isfile(STOCK_NAMES_FILE_PATH):
        with open(STOCK_NAMES_FILE_PATH) as stock_names_file:
            stocks = json.load(stock_names_file)
            filtered_stocks = []
            for stock in stocks:
                current_symbol = to_string(stock['symbol'])
                if symbol != current_symbol:
                    filtered_stocks.append(stock)
            filtered_stocks_json = json.dumps(filtered_stocks)
            stock_names_file = open(STOCK_NAMES_FILE_PATH, "w")
            stock_names_file.write(filtered_stocks_json)
            stock_names_file.close()


def get_stock_symbols(limit):
    symbols = []
    if os.path.isfile(STOCK_NAMES_FILE_PATH):
        with open(STOCK_NAMES_FILE_PATH) as stock_names_file:
            stock_names = json.load(stock_names_file)
            i = 1
            for stock in stock_names:
                if limit != 0 and limit < i:
                    break
                symbols.append(to_string(stock['symbol']))
                i += 1
    return symbols


def get_stock_data_by_symbol(symbol, date_from = None, date_to = None):
    stocks = pd.read_csv(FOLDER + symbol + '.csv', index_col='date', parse_dates=True)

    if date_from or date_to:
        stocks = stocks.loc[date_from:date_to]

    return stocks


def get_stock_data_by_symbols(symbols, date_from = None, date_to = None):
    stock_datas = []
    valid_symbols = []
    for symbol in symbols:
        stocks = get_stock_data_by_symbol(symbol, date_from, date_to)
        stock_datas.append(stocks['close'])
        valid_symbols.append(symbol)

    stocks = pd.concat(stock_datas, axis=1)
    stocks.columns = valid_symbols

    return stocks
