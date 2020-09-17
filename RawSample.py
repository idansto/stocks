class RawSample:
    ticker = None
    date = None
    sample = None

    def __init__(self, ticker, date, sample):
        self.ticker = ticker
        self.date = date
        self.sample = sample
