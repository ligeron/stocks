from data_provider import to_string


class Stock:
    def __init__(self, stock_info, quotes, calculations):
        self.company_name = to_string(stock_info['companyName'])
        self.website = to_string(stock_info['website'])
        self.sector = to_string(stock_info['sector'])
        self.symbol = to_string(stock_info['symbol'])
        self.exchange = to_string(stock_info['exchange'])
        self.ceo = to_string(stock_info['CEO'])
        self.issue_type = to_string(stock_info['issueType'])
        self.industry = to_string(stock_info['industry'])

        self.quotes = quotes
        self.ret = calculations['ret']
        self.sharpe = calculations['sharpe']
        self.vol = calculations['vol']

    def get_quotes(self, date_from=None, date_to=None):
        if date_from or date_to:
            return self.quotes.loc[date_from:date_to]
        return self.quotes

    def get_close_quote_by_date(self, date):
        quotes = self.get_quotes(date, date)
        if len(quotes.values) != 0:
            return quotes['close'].values[0]
        else:
            return None
