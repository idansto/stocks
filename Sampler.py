import yfinance as yf
from SamplerDao import *
from src.dao.samplesDAO import get_samples


def get_dates_between(start_date, end_date):  # TODO
    return ["2020-03-30", "2020-06-30"]


class Sampler:
    # sampler_dao = SamplerDao()

    def get_samples_and_responses(self, source):
        X = []
        y = []
        companies_ids = [1, 4, 9, 22]
        start_date = "2020-03-30"
        end_date = "2020-06-30"
        date_list = get_dates_between(start_date, end_date)
        features_ids = [3, 6]
        # raw_samples = self.sampler_dao.get_samples(companies_ids, start_date, end_date, features_ids)
        raw_samples = get_samples(companies_ids, features_ids, date_list)

        for raw_sample in raw_samples:
            if self.validate_sample(raw_sample):
                response = self.get_response(raw_sample.company_id, raw_sample.date)
                X.append(raw_sample.sample)
                y.append(response)

        return X, y

    @staticmethod
    def get_response(ticker, date):
        data = yf.download(ticker, start=date, end=date, period="1d", interval="1d")
        print(data)
        return float(data["Open"])

    @staticmethod
    def validate_sample(sample):
        return True
