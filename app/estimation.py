from data_provider import get_stock_symbols, get_stock_data_by_symbols
import numpy as np
from settings import *
from data_provider import to_string
from scipy.optimize import minimize

NUM_PORTS = 1000


class Estimation:
    stocks = None

    def __init__(self):
        symbols = self.get_best_stocks(30).values()
        self.stocks = get_stock_data_by_symbols(symbols)

    def main(self):
        print self.sharped_ratio_eval_random(self.stocks).max()

    def get_ret_vol_sr(self, weights):
        log_ret = np.log(self.stocks / self.stocks.shift(1))
        weights = np.array(weights)
        ret = np.sum(log_ret.mean() * weights) * 252
        vol = np.sqrt(np.dot(weights.T, np.dot(log_ret.cov() * 252, weights)))
        sr = ret / vol
        return np.array([ret, vol, sr])

    def neg_sharpe(self, weights):
        return self.get_ret_vol_sr(weights)[2] * -1

    def check_sum(self, weights):
        return np.sum(weights) - 1

    def minimize_volatility(self, weights):
        return self.get_ret_vol_sr(weights)[1]

    def sharped_ratio_eval_minimizer(self):
        stocks_count = len(self.stocks.columns)
        frontier_y = np.linspace(0, 0.3, 3)
        frontier_volatility = []

        for possible_return in frontier_y:
            # function for return
            cons = ({'type': 'eq', 'fun': self.check_sum},
                    {'type': 'eq', 'fun': lambda w: self.get_ret_vol_sr(w)[0] - possible_return})
            bound_template = (0, 1)
            i = 0
            guess = 1 / float(stocks_count)
            bounds = []
            init_guess = []
            while i < stocks_count:
                bounds.append(bound_template)
                init_guess.append(guess)
                i += 1

            bounds = tuple(bounds)

            result = minimize(self.minimize_volatility, init_guess, method='SLSQP', bounds=bounds, constraints=cons)

            frontier_volatility.append(result['fun'])
        print frontier_volatility

    def get_sharped_ratio_by_stock(self, symbol):
        stocks = get_stock_data_by_symbols([symbol])
        log_ret = np.log(stocks / stocks.shift(1))
        ret_arr = np.sum((log_ret.mean() * 1) * 252)
        vol_arr = np.sqrt(np.dot(1, np.dot(log_ret.cov() * 252, 1)))
        sharpe_arr = ret_arr / vol_arr

        return sharpe_arr.max()

    def sharped_ratio_eval_random(self, stocks):
        log_ret = np.log(stocks / stocks.shift(1))
        all_weights = np.zeros((NUM_PORTS, len(stocks.columns)))
        ret_arr = np.zeros(NUM_PORTS)
        vol_arr = np.zeros(NUM_PORTS)
        sharpe_arr = np.zeros(NUM_PORTS)

        for ind in range(NUM_PORTS):
            weights = np.array(np.random.random(len(stocks.columns)))
            weights = weights / np.sum(weights)
            all_weights[ind, :] = weights
            ret_arr[ind] = np.sum((log_ret.mean() * weights) * 252)
            vol_arr[ind] = np.sqrt(np.dot(weights.T, np.dot(log_ret.cov() * 252, weights)))
            sharpe_arr[ind] = ret_arr[ind] / vol_arr[ind]

        return sharpe_arr

    def get_best_stocks(self, limit):
        if os.path.isfile(SR_FILE_PATH):
            with open(SR_FILE_PATH) as file:
                sorted_stocks = json.load(file)
        else:
            sorted_stocks = {}
            symbols = get_stock_symbols(0)[1:2500]
            for symbol in symbols:
                sorted_stocks[self.get_sharped_ratio_by_stock(symbol)] = symbol
            file = open(SR_FILE_PATH, "w")
            file.write(json.dumps(sorted_stocks))
            file.close()

        i = 1
        result = {}
        for key in sorted(sorted_stocks, reverse=True):
            if i > limit:
                break
            result[key] = to_string(sorted_stocks[key])
            i += 1

        return result


x = Estimation()
x.sharped_ratio_eval_minimizer()
