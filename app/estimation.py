from data_provider import get_stock_symbols, get_stock_data_by_symbols
import numpy as np
from settings import *
from data_provider import to_string

NUM_PORTS = 10000


class Estimation:
    stocks = None
    date_from = None
    date_to = None

    def __init__(self, date_from, date_to):
        self.date_from = date_from
        self.date_to = date_to
        symbols = self.get_best_stocks(10)
        self.stocks = get_stock_data_by_symbols(symbols, date_from=self.date_from, date_to=self.date_to)

    def get_sharped_ratio_by_stock(self, symbol):
        stocks = get_stock_data_by_symbols([symbol])
        log_ret = np.log(stocks / stocks.shift(1))
        ret_arr = np.sum((log_ret.mean() * 1) * 252)
        vol_arr = np.sqrt(np.dot(1, np.dot(log_ret.cov() * 252, 1)))
        sharpe_arr = ret_arr / vol_arr

        return {"symbol": symbol, "ret": ret_arr, "vol": vol_arr.max(), "sharpe": sharpe_arr.max()}

    def sharped_ratio_eval_random(self):
        log_ret = np.log(self.stocks / self.stocks.shift(1))
        all_weights = np.zeros((NUM_PORTS, len(self.stocks.columns)))
        ret_arr = np.zeros(NUM_PORTS)
        vol_arr = np.zeros(NUM_PORTS)
        sharpe_arr = np.zeros(NUM_PORTS)

        for ind in range(NUM_PORTS):
            weights = np.array(np.random.random(len(self.stocks.columns)))
            weights = weights / np.sum(weights)
            all_weights[ind, :] = weights
            ret_arr[ind] = np.sum((log_ret.mean() * weights) * 252)
            vol_arr[ind] = np.sqrt(np.dot(weights.T, np.dot(log_ret.cov() * 252, weights)))
            sharpe_arr[ind] = ret_arr[ind] / vol_arr[ind]

        return (sharpe_arr, all_weights, ret_arr)

    def get_best_stocks(self, limit):
        if os.path.isfile(SR_FILE_PATH):
            with open(SR_FILE_PATH) as file:
                stock_params = json.load(file)
        else:
            stock_params = []
            symbols = get_stock_symbols(2000)
            for symbol in symbols:
                stock_params.append(self.get_sharped_ratio_by_stock(symbol))
            file = open(SR_FILE_PATH, "w")
            file.write(json.dumps(stock_params))
            file.close()

        stocks_sorted_by_ret = sorted(stock_params, key=lambda x: x['ret'], reverse=True)[:500]
        stocks_sorted_by_sharpe = sorted(stocks_sorted_by_ret, key=lambda x: x['sharpe'], reverse=True)[:limit]

        result = []
        for stock_param in stocks_sorted_by_sharpe:
            result.append(to_string(stock_param['symbol']))

        return result
#
#
# est = Estimation('2017-01-03', '2018-01-03')
# sharpe_arr, all_weights, ret_arr = est.sharped_ratio_eval_random()
# print est.stocks.columns
#
# print sharpe_arr.max()
# arg_max = sharpe_arr.argmax()
# print all_weights[arg_max, :]

