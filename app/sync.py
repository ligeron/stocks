import json
import pandas_datareader as web
import requests
from settings import *
from data_provider import to_string, delete_symbol


def save_stocks(skip_exists):
    # Get stock names
    if os.path.isfile(STOCK_NAMES_FILE_PATH):
        with open(STOCK_NAMES_FILE_PATH) as stock_names_file:
            stock_names = json.load(stock_names_file)
    else:
        response = requests.get(STOCKS_URL)
        stock_names_json = response.content
        stock_names_file = open(STOCK_NAMES_FILE_PATH, "w")
        stock_names_file.write(stock_names_json)
        stock_names_file.close()
        stock_names = json.loads(stock_names_json)

    data = stock_names
    count_stoks = len(data)
    print(count_stoks)
    first_valid_date = None

    for stock in data:
        symbol = to_string(stock['symbol'])
        name = to_string(stock['name'])
        file_path = FOLDER + symbol + '.csv'

        if skip_exists and os.path.isfile(file_path):
            print('file for ' + name + ' already exists')
            continue

        try:
            stock_data = web.DataReader(symbol, CHANNEL, DATE_FROM, DATE_TO)
            if first_valid_date and first_valid_date != stock_data.first_valid_index():
                delete_symbol(symbol)
                continue
            else:
                first_valid_date = stock_data.first_valid_index()
        except Exception:
            delete_symbol(symbol)
            continue

        try:
            stock_data.to_csv(file_path)
        except Exception:
            delete_symbol(symbol)

        print(name + ' was saved')


save_stocks(True)
