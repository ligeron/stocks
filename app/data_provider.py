import pandas as pd
from settings import *
import json
import unicodedata
import requests


def to_string(u_string):
    if not isinstance(u_string, unicode):
        return u_string
    return unicodedata.normalize('NFKD', u_string).encode('ascii', 'ignore')


def delete_symbol(symbol, multiple=False):
    if os.path.isfile(STOCK_NAMES_FILE_PATH):
        with open(STOCK_NAMES_FILE_PATH) as stock_names_file:
            stocks = json.load(stock_names_file)
            filtered_stocks = []
            for stock in stocks:
                current_symbol = to_string(stock['symbol'])
                if (multiple and (current_symbol not in symbol)) or (not multiple and symbol != current_symbol):
                    filtered_stocks.append(stock)
            filtered_stocks_json = json.dumps(filtered_stocks)
            stock_names_file = open(STOCK_NAMES_FILE_PATH, "w")
            stock_names_file.write(filtered_stocks_json)
            stock_names_file.close()
            print (symbol)
            print('Was deleted')


def get_url_content(url, verbose=False):
    try:
        result = json.loads(requests.get(url).content)
        if verbose:
            print(url + ' was opened')
    except Exception:
        return None

    return result


def get_stock_symbols(limit=None):
    symbols = []

    stock_names = get_stocks_data()
    i = 1
    for stock in stock_names:
        if limit and limit < i:
            break
        symbols.append(to_string(stock['symbol']))
        i += 1

    return symbols


def get_stocks_data():
    if os.path.isfile(STOCK_NAMES_FILE_PATH):
        with open(STOCK_NAMES_FILE_PATH) as stock_names_file:
            return json.load(stock_names_file)


def get_stock_data_by_symbol(symbol, date_from=None, date_to=None):
    stocks = pd.read_csv(FOLDER + symbol + '.csv', index_col='date', parse_dates=True)

    if date_from or date_to:
        stocks = stocks.loc[date_from:date_to]

    return stocks


def get_stock_data_by_symbols(symbols, date_from=None, date_to=None):
    stock_datas = []
    valid_symbols = []
    for symbol in symbols:
        stocks = get_stock_data_by_symbol(symbol, date_from, date_to)
        stock_datas.append(stocks['close'])
        valid_symbols.append(symbol)

    stocks = pd.concat(stock_datas, axis=1)
    stocks.columns = valid_symbols

    return stocks


def get_distinct_attribute(attribute_name):
    attribute_options = []
    data = get_stocks_data()
    for stock in data:
        option = to_string(stock[attribute_name])
        if not option in attribute_options:
            attribute_options.append(option)

    return attribute_options
