from portfolio_set import PortfolioSet
from datetime import timedelta
from json import JSONEncoder
from settings import *


class MyEncoder(JSONEncoder):
    def default(self, o):
        return o.__dict__


amount = 10000
DATE_MASK = '%Y-%m-%d'

buy_date = '2017-01-05'
sell_date = '2018-01-04'
buy_date_obj = datetime.strptime(buy_date, DATE_MASK)
sell_date_obj = datetime.strptime(sell_date, DATE_MASK)

ps = PortfolioSet('2016-01-13', '2017-01-03', total_stocks_count=20, portfolios_count=3)

print 'Calculate weights...'
ps.process_weights()
print 'Calculate sell dynamic...'

current_sell_date_obj = datetime.strptime(buy_date, DATE_MASK)
while current_sell_date_obj < sell_date_obj:
    for portfolio in ps.portfolios:
        portfolio.investments_amount = amount
        portfolio.buy_date = buy_date
        portfolio.calculate_number_of_stocks(rebalance=True)
        portfolio.add_portfolio_rev(current_sell_date_obj.strftime(DATE_MASK))
    current_sell_date_obj = current_sell_date_obj + timedelta(days=1)

result_file = open(RESULT_FILE_PATH, "w")
result_file.write(MyEncoder().encode(ps))
result_file.close()
