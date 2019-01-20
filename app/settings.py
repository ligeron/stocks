from datetime import datetime
import os

STOCKS_URL = 'https://api.iextrading.com/1.0/ref-data/symbols'
CHANNEL = 'iex'

STOCKS_FOLDER = 'files/stocks'
STOCK_NAMES_FILE = 'stock_names.json'

DATE_FROM = datetime(2017, 1, 1)
DATE_TO = datetime(2019, 12, 22)

FOLDER = os.path.dirname(os.path.abspath(__file__)) + '/' + STOCKS_FOLDER + '/'
STOCK_NAMES_FILE_PATH = FOLDER + STOCK_NAMES_FILE
