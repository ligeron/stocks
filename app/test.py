from ml import *

ticker = 'RCL'
test_size = 0.25

predictions, test_df = do_ml(ticker, test_size=test_size)

i = 0
money = 10000
first_buy = False
number_of_stocks = 0
transaction_price = 2.5
transaction_spends = 0

for date, row in test_df.iterrows():
    price = row[ticker]
    decision = predictions[i]
    i += 1
    if decision == -1 and not first_buy:
        continue
    if decision == 1:
        if money == 0:
            continue
        number_of_stocks = money / price
        money = 0
        transaction_spends += transaction_price
    if decision == -1:
        if number_of_stocks == 0:
            continue
        money = number_of_stocks * price
        number_of_stocks = 0
        transaction_spends += transaction_price
    if decision == 0:
        continue

    first_buy = True

if money == 0:
    money = price * number_of_stocks

print money
print transaction_spends
