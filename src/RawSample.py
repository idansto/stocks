class RawSample:
    company_id = None
    date = None
    sample = None

    def __init__(self, company_id, date, sample):
        self.company_id = company_id
        self.ticker = "MSFT"
        self.date = date
        self.sample = sample

    def __str__(self):
        return "company_id = {}, date = {}, sample = {}".format(self.company_id, self.date, self.sample)

    def __repr__(self):
        return self.__str__()
