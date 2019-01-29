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

        self.investments_amount = 0
        self.buy_date = '2019-01-03'

        self.number_of_stocks = {}

        self.rev_dynamic = {}
        self.rev_dynamic_stocks = {}

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

    def calculate_number_of_stocks(self):
        for symbol, stock in self.stocks.iteritems():
            weight = self.weights[symbol]
            buy_money = weight * self.investments_amount
            buy_price = stock.get_close_quote_by_date(self.buy_date)
            self.number_of_stocks[symbol] = buy_money / buy_price

    def add_portfolio_rev(self, sell_date):
        total = 0
        for symbol, stock in self.stocks.iteritems():
            sell_price = stock.get_close_quote_by_date(sell_date)
            if not sell_price:
                return
            if not symbol in self.number_of_stocks:
                raise Exception('Please call calculate_number_of_stocks method firstly')
            number_of_stocks = self.number_of_stocks[symbol]
            sell_money = sell_price * number_of_stocks
            if sell_date not in dict.keys(self.rev_dynamic_stocks):
                self.rev_dynamic_stocks[sell_date] = {}
            self.rev_dynamic_stocks[sell_date][symbol] = sell_money
            total += sell_money
        self.rev_dynamic[sell_date] = total
