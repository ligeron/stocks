from estimation import Estimation
import random
from portfolio import Portfolio


class PortfolioSet:
    def __init__(self, date_from, date_to, total_stocks_count=100, portfolios_count=10):
        self.portfolios = []
        self.init(date_from, date_to, portfolios_count, total_stocks_count)

    def init(self, date_from, date_to, portfolios_count, total_stocks_count):
        est = Estimation(date_from, date_to)
        best_stocks = est.get_best_stocks(total_stocks_count)
        stocks_count = total_stocks_count / portfolios_count
        portfolio_number = portfolios_count
        while portfolio_number > 0:
            stock_number = stocks_count
            portfolio = Portfolio(date_from, date_to)
            while stock_number > 0:
                index = random.randint(0, len(best_stocks) - 1)
                portfolio.add_stock(best_stocks[index])
                del best_stocks[index]
                stock_number -= 1
            self.portfolios.append(portfolio)
            portfolio_number -= 1

    def process_weights(self):
        for portfolio in self.portfolios:
            portfolio.process_weights()

    def get_best_portfolios(self, limit):
        best_portfolios = self.portfolios.sort(key=lambda x: x.sharpe, reverse=True)
        return best_portfolios[:limit]
