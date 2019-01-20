from data_provider import get_stock_symbols, get_stock_data_by_symbols
import numpy as np

NUM_PORTS = 1


def main():
    symbols = get_stock_symbols(0)[100:101]
    stocks = get_stock_data_by_symbols(symbols)
    print stocks

    print sharped_ratio_eval_random(stocks)


def get_sharped_ratio_by_stock(symbol):
    stocks = get_stock_data_by_symbols([symbol])
    log_ret = np.log(stocks / stocks.shift(1))
    ret_arr = np.sum((log_ret.mean() * 1) * 252)
    vol_arr = np.sqrt(np.dot(1, np.dot(log_ret.cov() * 252, 1)))
    sharpe_arr = ret_arr / vol_arr

    return sharpe_arr.max()


def sharped_ratio_eval_random(stocks):
    log_ret = np.log(stocks / stocks.shift(1))
    all_weights = np.zeros((NUM_PORTS, len(stocks.columns)))
    ret_arr = np.zeros(NUM_PORTS)
    vol_arr = np.zeros(NUM_PORTS)
    sharpe_arr = np.zeros(NUM_PORTS)

    for ind in range(NUM_PORTS):
        # Create Random Weights
        weights = np.array(np.random.random(len(stocks.columns)))

        # Rebalance Weights
        weights = weights / np.sum(weights)

        # Save Weights
        all_weights[ind, :] = weights

        # Expected Return
        ret_arr[ind] = np.sum((log_ret.mean() * weights) * 252)

        # Expected Variance
        vol_arr[ind] = np.sqrt(np.dot(weights.T, np.dot(log_ret.cov() * 252, weights)))

        # Sharpe Ratio
        sharpe_arr[ind] = ret_arr[ind] / vol_arr[ind]

    return sharpe_arr.max()
    # return all_weights[sharpe_arr.argmax(),:]


def get_best_stocks(limit):
    sorted_stocks = {}
    symbols = get_stock_symbols(0)[1:500]
    for symbol in symbols:
        sorted_stocks[get_sharped_ratio_by_stock(symbol)] = symbol
    i = 1
    result = {}
    for key in sorted(sorted_stocks, reverse=True):
        if i > limit:
            break
        result[key] = sorted_stocks[key]
        i += 1
    return result

# main()
x = get_best_stocks(4)
x = get_best_stocks(4)