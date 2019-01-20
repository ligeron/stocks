from data_provider import get_stock_symbols, get_stock_data_by_symbols

symbols = get_stock_symbols(5)
print get_stock_data_by_symbols(symbols)


