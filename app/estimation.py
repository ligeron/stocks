from data_provider import get_stock_symbols, get_stock_data_by_symbols, get_stock_data_by_symbol, get_stocks_info, \
    to_string
import numpy as np
from settings import *
import json
from stock import Stock


class Estimation:
    def __init__(self, date_from, date_to, stocks_count=15, iterations_number=1000, stocks_with_max_ret=500):
        self.iterations_number = iterations_number
        self.stocks_count = stocks_count
        self.stocks_with_max_ret = stocks_with_max_ret
        self.date_from = date_from
        self.date_to = date_to
        self.stock_infos = {}
        infos = get_stocks_info()
        for info in infos:
            self.stock_infos[to_string(info['symbol'])] = info

    def get_sharped_ratio_by_stock(self, symbol):
        stocks = get_stock_data_by_symbols([symbol])
        log_ret = np.log(stocks / stocks.shift(1))
        ret_arr = np.sum((log_ret.mean() * 1) * 252)
        vol_arr = np.sqrt(np.dot(1, np.dot(log_ret.cov() * 252, 1)))
        sharpe_arr = ret_arr / vol_arr

        return {"symbol": symbol, "ret": ret_arr, "vol": vol_arr.max(), "sharpe": sharpe_arr.max()}

    def get_best_stocks(self, limit):
        if os.path.isfile(SR_FILE_PATH):
            with open(SR_FILE_PATH) as file:
                stock_params = json.load(file)
        else:
            stock_params = []
            symbols = get_stock_symbols()
            for symbol in symbols:
                stock_params.append(self.get_sharped_ratio_by_stock(symbol))
            file = open(SR_FILE_PATH, "w")
            file.write(json.dumps(stock_params))
            file.close()

        stocks_sorted_by_ret = sorted(stock_params, key=lambda x: x['ret'], reverse=True)[:self.stocks_with_max_ret]
        stocks_sorted_by_sharpe = sorted(stocks_sorted_by_ret, key=lambda x: x['sharpe'], reverse=True)[:limit]

        result = []

        for stock_param in stocks_sorted_by_sharpe:
            info = self.get_stock_info_by_symbol(stock_param['symbol'])
            quotes = get_stock_data_by_symbol(stock_param['symbol'])
            stock = Stock(info, quotes, stock_param)
            result.append(stock)

        return result

    def get_stock_info_by_symbol(self, symbol):
        for current_symbol, info in self.stock_infos.iteritems():
            if symbol == current_symbol:
                return info
