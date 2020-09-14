import yfinance as yf


class Sampler:
    dao = DAO()

    def get_samples_and_responses(self, source):
        X = []
        y = []
        raw_samples = self.dao.getSamples(companies_ids, start_date, end_date, features_ids)

        for raw_sample in raw_samples:
            if self.validate_sample(raw_sample):
                response = self.get_response(raw_sample.ticker, raw_sample.date)
                X.append(raw_sample.sample)
                y.append(response)

        return X, y

    @staticmethod
    def get_response(ticker, date):
        yf.download(ticker, start=date, period="1d", interval="1d")
        return 150.00

    @staticmethod
    def validate_sample(sample):
        return True
