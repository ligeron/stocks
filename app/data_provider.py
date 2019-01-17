import pandas as pd
from sync import *


def get_stock_symbols(limit):
    stock_names_file_path = FOLDER + STOCK_NAMES_FILE
    symbols = []
    if os.path.isfile(stock_names_file_path):
        with open(stock_names_file_path) as stock_names_file:
            stock_names = json.load(stock_names_file)
            i = 0
            for stock in stock_names:
                if limit < i:
                    break
                symbols.append(to_string(stock['symbol']))
                i += 1
    return symbols


def get_stock_data_by_symbol(symbol):
    return pd.read_csv(FOLDER + symbol + '.csv', index_col='date', parse_dates=True)


def get_stock_data_by_symbols(symbols):
    stock_datas = []
    date = None
    valid_symbols = []
    for symbol in symbols:
        stocks = get_stock_data_by_symbol(symbol)
        if date and date != stocks.first_valid_index():
            continue
        else:
            date = stocks.first_valid_index()

        stock_datas.append(stocks['close'])
        valid_symbols.append(symbol)

    stocks = pd.concat(stock_datas, axis=1)
    stocks.columns = valid_symbols

    return stocks