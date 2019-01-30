from data_provider import get_stock_symbols, get_stock_data_by_symbols, get_stock_data_by_symbol, get_stocks_info, \
    to_string
import numpy as np
from settings import *
import json
from stock import Stock
import operator


class Estimation:
    def __init__(self, date_from, date_to, iterations_number=1000, stocks_with_max_ret=100):
        self.iterations_number = iterations_number
        self.stocks_with_max_ret = stocks_with_max_ret
        self.date_from = date_from
        self.date_to = date_to
        self.stock_infos = {}
        infos = get_stocks_info()
        for info in infos:
            self.stock_infos[to_string(info['symbol'])] = info

    def get_sharped_ratio_by_stock(self, symbol):
        stocks = get_stock_data_by_symbols([symbol], self.date_from, self.date_to)
        if stocks is None:
            return None
        log_ret = np.log(stocks / stocks.shift(1))
        ret_arr = np.sum((log_ret.mean() * 1) * 252)
        vol_arr = np.sqrt(np.dot(1, np.dot(log_ret.cov() * 252, 1)))
        sharpe_arr = ret_arr / vol_arr

        return {"symbol": symbol, "ret": ret_arr, "vol": vol_arr.max(), "sharpe": sharpe_arr.max()}

    def get_best_stocks(self, limit):
        if not os.path.exists(SR_FOLDER_PATH):
            os.makedirs(SR_FOLDER_PATH)
        file_name = SR_FOLDER_PATH + self.date_from + '-' + self.date_to + '.json'
        if os.path.isfile(file_name):
            with open(file_name) as file:
                stock_params = json.load(file)
        else:
            print('Create cache for new estimation period from ' + self.date_from + ' to ' + self.date_to + '...')
            stock_params = []
            symbols = get_stock_symbols()

            for symbol in symbols:
                stock_param = self.get_sharped_ratio_by_stock(symbol)
                if stock_param is not None:
                    stock_params.append(stock_param)
            file = open(file_name, "w")
            file.write(json.dumps(stock_params))
            file.close()

        stocks_sorted_by_ret = sorted(stock_params, key=lambda x: x['ret'], reverse=True)[:self.stocks_with_max_ret]
        stocks_sorted_by_sharpe = sorted(stocks_sorted_by_ret, key=lambda x: x['sharpe'], reverse=True)
        first_10 = stocks_sorted_by_sharpe[:10]
        valid_count = self.get_valid_count(first_10)
        result = []
        current_stock_index = 0
        while len(result) < limit:
            stock_param = stocks_sorted_by_sharpe[current_stock_index]
            current_stock_index += 1
            quotes = get_stock_data_by_symbol(stock_param['symbol'])
            if len(quotes) != valid_count:
                continue
            info = self.get_stock_info_by_symbol(stock_param['symbol'])
            stock = Stock(info, quotes, stock_param)
            result.append(stock)

        return result

    def get_valid_count(self, first_10):
        counts = {}
        for stock_param in first_10:
            quotes = get_stock_data_by_symbol(stock_param['symbol'])
            quotes_count = len(quotes)
            if quotes_count in counts:
                counts[quotes_count] += 1
            else:
                counts[quotes_count] = 1
        return max(counts.iteritems(), key=operator.itemgetter(1))[0]

    def quotes_is_valid(self, quotes):
        list = quotes['close'].values.tolist()
        for row in list:
            if not row:
                return False
        return True

    def get_stock_info_by_symbol(self, symbol):
        for current_symbol, info in self.stock_infos.iteritems():
            if symbol == current_symbol:
                return info
