import pandas as pd
import numpy as np
from settings import RANDOM_SEED


class Portfolio:
    def __init__(self, date_from, date_to):
        self.stocks = {}
        self.date_from = date_from
        self.date_to = date_to
        self.iterations_number = 1000
        self.ret = None
        self.vol = None
        self.sharpe = None
        self.weights = None
        self.rev_dynamic = {}

    def add_stock(self, stock):
        self.stocks[stock.symbol] = stock

    def process_weights(self):
        stocks = self.get_stock_data()
        log_ret = np.log(stocks / stocks.shift(1))
        all_weights = np.zeros((self.iterations_number, len(stocks.columns)))
        ret_arr = np.zeros(self.iterations_number)
        vol_arr = np.zeros(self.iterations_number)
        sharpe_arr = np.zeros(self.iterations_number)
        np.random.seed(RANDOM_SEED)

        for ind in range(self.iterations_number):
            weights = np.array(np.random.random(len(stocks.columns)))
            weights = weights / np.sum(weights)
            all_weights[ind, :] = weights
            ret_arr[ind] = np.sum((log_ret.mean() * weights) * 252)
            vol_arr[ind] = np.sqrt(np.dot(weights.T, np.dot(log_ret.cov() * 252, weights)))
            sharpe_arr[ind] = ret_arr[ind] / vol_arr[ind]

        best_weights_index = sharpe_arr.argmax()
        self.ret = ret_arr[best_weights_index]
        self.vol = vol_arr[best_weights_index]
        self.sharpe = sharpe_arr[best_weights_index]

        weights = all_weights[best_weights_index, :].tolist()
        symbols = stocks.columns.values.tolist()
        self.weights = dict(zip(symbols, weights))

    def get_stock_data(self):
        stock_datas = []
        stock_symbols = []
        for stock in self.stocks.values():
            stock_datas.append(stock.get_quotes(self.date_from, self.date_to)['close'])
            stock_symbols.append(stock.symbol)

        stocks = pd.concat(stock_datas, axis=1)
        stocks.columns = stock_symbols

        return stocks

    def add_portfolio_rev(self, buy_date, sell_date, investments_amount):
        total = 0
        for symbol, stock in self.stocks.iteritems():
            weight = self.weights[symbol]
            buy_money = weight * investments_amount
            buy_price = stock.get_close_quote_by_date(buy_date)
            sell_price = stock.get_close_quote_by_date(sell_date)
            if not buy_price or not sell_price:
                return
            number_fo_stocks = buy_money / buy_price
            sell_money = sell_price * number_fo_stocks
            total += sell_money
        self.rev_dynamic[sell_date] = total


