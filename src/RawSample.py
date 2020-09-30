class RawSample:

    def __init__(self, company_id, ticker, date, sample):
        self.company_id = company_id
        self.ticker = ticker
        self.date = date
        self.sample = sample

    def __str__(self):
        return "company_id = {}, ticker = {}, date = {}, sample = {}".format(self.company_id, self.ticker, self.date, self.sample)

    def __repr__(self):
        return self.__str__()
