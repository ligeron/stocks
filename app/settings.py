from datetime import datetime
import os

IEX_API_SITE = 'https://api.iextrading.com/1.0/'
STOCKS_URL = IEX_API_SITE + 'ref-data/symbols'
COMPANY_URL = IEX_API_SITE + 'stock/{0}/company'
CHANNEL = 'iex'

STOCKS_FOLDER = 'files/stocks'
STOCK_NAMES_FILE = '!stock_names.json'
SR_FILE = '!sr_by_company.json'

DATE_FROM = datetime(2017, 1, 1)
DATE_TO = datetime(2019, 12, 22)

RANDOM_SEED = 11

FOLDER = os.path.dirname(os.path.abspath(__file__)) + '/' + STOCKS_FOLDER + '/'
FOLDER_HTML = os.path.dirname(os.path.abspath(__file__)) + '/html/'
STOCK_NAMES_FILE_PATH = FOLDER + STOCK_NAMES_FILE
RESULT_FILE_PATH = FOLDER_HTML + 'result.json'
SR_FILE_PATH = FOLDER + SR_FILE
