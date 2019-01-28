from portfolio_set import PortfolioSet
from datetime import datetime
from datetime import timedelta
from json import JSONEncoder
from settings import *


class MyEncoder(JSONEncoder):
    def default(self, o):
        return o.__dict__


amount = 100000
DATE_MASK = '%Y-%m-%d'

buy_date = '2018-01-03'
sell_date = '2018-05-03'
buy_date_obj = datetime.strptime(buy_date, DATE_MASK)
sell_date_obj = datetime.strptime(sell_date, DATE_MASK)

ps = PortfolioSet('2017-01-03', '2018-01-03', total_stocks_count=30, portfolios_count=5)
print 'Calculate weights...'
ps.process_weights()

print 'Calculate sell dynamic...'
current_sell_date_obj = datetime.strptime(buy_date, DATE_MASK)
while current_sell_date_obj < sell_date_obj:
    for portfolio in ps.portfolios:
        portfolio.add_portfolio_rev(buy_date, current_sell_date_obj.strftime(DATE_MASK), 100000)
    current_sell_date_obj = current_sell_date_obj + timedelta(days=1)

result_file = open(RESULT_FILE_PATH, "w")
result_file.write(MyEncoder().encode(ps))
result_file.close()
