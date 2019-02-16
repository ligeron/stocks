import pandas_datareader as web
import requests
from settings import *
from data_provider import to_string, delete_symbol, get_stock_symbols, get_url_content
from concurrent.futures import ThreadPoolExecutor as PoolExecutor
import json
import bs4 as bs


def save_stocks(skip_exists=True):
    if not os.path.isfile(STOCK_NAMES_FILE_PATH):
        stock_names = get_url_content(STOCKS_URL)
        companies = []
        urls = []
        best_symbols = save_sp500_tickers()
        for stock_data in stock_names:
            symbol = to_string(stock_data['symbol'])
            if symbol not in best_symbols:
                continue
            urls.append(COMPANY_URL.format(symbol))

        with PoolExecutor(max_workers=30) as executor:
            for result in executor.map(lambda url: get_url_content(url, False), urls):
                if result and result['sector'] != '' and result['sector'] != None:
                    companies.append(result)
                print result

        stock_names_file = open(STOCK_NAMES_FILE_PATH, "w")
        stock_names_file.write(json.dumps(companies))
        stock_names_file.close()

    symbols = get_stock_symbols()
    symbols_to_delete = []
    with PoolExecutor(max_workers=30) as executor:
        for _ in executor.map(lambda s: save_stock_data(s, symbols_to_delete, skip_exists), symbols):
            pass
    print('Symbols to delete:')
    print(symbols_to_delete)
    delete_symbol(symbols_to_delete, multiple=True)

    print('Finish')


def save_stock_data(symbol, symbols_to_delete, skip_exists=True):
    try:
        stock_data = web.DataReader(symbol, CHANNEL, DATE_FROM, DATE_TO)
    except Exception as e:
        symbols_to_delete.append(symbol)
        return
    else:
        file_path = FOLDER + symbol + '.csv'
        if skip_exists and os.path.isfile(file_path):
            print('file for ' + symbol + ' already exists')
            return
        else:
            try:
                stock_data.to_csv(file_path)
            except Exception as e:
                symbols_to_delete.append(symbol)
                return
            print('file for ' + symbol + ' was saved successfully')


def save_sp500_tickers():
    resp = requests.get('https://en.wikipedia.org/wiki/List_of_S%26P_500_companies')
    soup = bs.BeautifulSoup(resp.text,  "lxml")
    table = soup.find('table', {'class':'wikitable sortable'})
    tickers = []
    for row in table.findAll('tr')[1:]:
        ticker = to_string(row.findAll('td')[1].text)
        tickers.append(ticker)

    return tickers


# print save_sp500_tickers()
save_stocks()
