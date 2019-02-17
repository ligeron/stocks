from collections import Counter
import numpy as np
import pandas as pd
from sklearn import svm, neighbors, model_selection
from sklearn.ensemble import VotingClassifier, RandomForestClassifier
from data_provider import get_stock_symbols

# tickers = get_stock_symbols(180)


def procces_data_for_lables(ticker):
    hm_days = 7
    df = pd.read_csv('sp500_joined_closses.csv', index_col=0)
    tickers = df.columns.values.tolist()
    df.fillna(0, inplace=True)
    main_df = pd.DataFrame()

    for i in range(1, hm_days + 1):
        df['{}_{}d'.format(ticker, i)] = (df[ticker].shift(-i) - df[ticker]) / df[ticker]

    df.fillna(0, inplace=True)

    return tickers, df


def buy_sell_hold(*args):
    cols = [c for c in args]
    requirment = 0.02
    for col in cols:
        if col > requirment:
            return 1
        if col < -requirment:
            return -1
    return 0


def extract_featuresets(ticker):
    tickers, df = procces_data_for_lables(ticker)

    df['{}_target'.format(ticker)] = list(map(buy_sell_hold,
                                              df['{}_1d'.format(ticker)],
                                              df['{}_2d'.format(ticker)],
                                              df['{}_3d'.format(ticker)],
                                              df['{}_4d'.format(ticker)],
                                              df['{}_5d'.format(ticker)],
                                              df['{}_6d'.format(ticker)],
                                              df['{}_7d'.format(ticker)]))

    vals = df['{}_target'.format(ticker)].values.tolist()
    str_vals = [str(i) for i in vals]
    print('Data spread:', Counter(str_vals))

    df.fillna(0, inplace=True)
    df = df.replace([np.inf, -np.inf], np.nan)
    df.dropna(inplace=True)

    df_vals = df[[ticker1 for ticker1 in tickers]].pct_change()
    df_vals = df_vals.replace([np.inf, -np.inf], 0)
    df_vals.fillna(0, inplace=True)

    X = df_vals.values
    y = df['{}_target'.format(ticker)].values

    return X, y, df


def do_ml(ticker, test_size=0.25):
    correlation_set, ticker_decision_set, df = extract_featuresets(ticker)
    lenght = len(ticker_decision_set)
    train_size = 1 - test_size
    train_lenght = int(round(train_size * lenght))
    test_lenght = lenght - train_lenght
    train_correlation_set = correlation_set[:train_lenght]
    train_ticker_decision_set = ticker_decision_set[:train_lenght]
    test_correlation_set = correlation_set[train_lenght:]
    test_ticker_decision_set = ticker_decision_set[train_lenght:]
    test_df = df.tail(test_lenght)

    clf = VotingClassifier([
                            ('lsvc', svm.LinearSVC()),
                            # ('knn', neighbors.KNeighborsClassifier()),
                            # ('rfor', RandomForestClassifier(n_estimators=100))
    ])
    clf.fit(train_correlation_set, train_ticker_decision_set)
    confidence = clf.score(test_correlation_set, test_ticker_decision_set)
    print('Accuracy', confidence)
    predictions = clf.predict(test_correlation_set)
    print('Predicted spread:', Counter(predictions))

    return predictions, test_df


