from estimation import Estimation
from data_provider import get_stock_data_by_symbol, print_attributes_by_symbol

est = Estimation('2017-01-03', '2018-01-03', stocks_count=3, iterations_number=1000)

amount = 100000

buy_date = '2018-01-03'
sell_date = '2019-01-03'
sharpe_arr, all_weights, ret_arr = est.sharped_ratio_eval_random()
columns = est.stocks.columns
weights = all_weights[sharpe_arr.argmax(), :]

stocks_with_weights = {}
i = 0
for column in columns.values.tolist():
    stocks_with_weights[column] = {"weight": weights[i]}
    i += 1

total = 0

for symbol in stocks_with_weights.keys():
    stocks_with_weights[symbol]['buy_money'] = stocks_with_weights[symbol]['weight'] * amount
    buy_price = get_stock_data_by_symbol(symbol, buy_date, buy_date)['close'].values[0]
    stocks_with_weights[symbol]['number_fo_stocks'] = stocks_with_weights[symbol]['buy_money'] / buy_price
    sell_price = get_stock_data_by_symbol(symbol, sell_date, sell_date)['close'].values[0]
    stocks_with_weights[symbol]['sell_money'] = sell_price * stocks_with_weights[symbol]['number_fo_stocks']
    total += stocks_with_weights[symbol]['sell_money']

print stocks_with_weights

print total

print (total / amount) * 100 - 100

for symbol in stocks_with_weights.keys():
    print_attributes_by_symbol(symbol, ['companyName', 'sector', 'industry','website'])
    print stocks_with_weights[symbol]

