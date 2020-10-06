import math

import yfinance as yf
import datetime

from sampler.dao.CompaniesDAO import get_tickers, get_companies_ids
from sampler.dao.FeaturesDAO import get_features_names
from src.sampler.dao.SamplesDAO import get_samples
import pandas as pd
from tqdm import tqdm

from utils.DateUtils import get_quraterly_dates_between, next_business_day, str_to_date


class Sampler:
    # sampler_dao = SamplerDao()

    # def get_samples_and_responses_old(self):
    #     print("builds samples and responses:" + '\n')
    #     X = []
    #     y = []
    #     companies_ids = [2]
    #     start_date = "2018-12-31"
    #     end_date = "2019-12-31"
    #     date_list = get_quraterly_dates_between(start_date, end_date)
    #     features_ids = [1, 2]
    #     # raw_samples = self.sampler_dao.get_samples(companies_ids, start_date, end_date, features_ids)
    #     raw_samples = get_samples(companies_ids, features_ids, date_list)
    #
    #     for raw_sample in tqdm(raw_samples):
    #         # print(raw_sample.date)
    #         if self.validate_sample(raw_sample):
    #             response = self.get_response(raw_sample.ticker, raw_sample.date)
    #             X.append(raw_sample.sample)
    #             y.append(response)
    #
    #     self.print_samples(X, y)
    #
    #     return X, y

    def get_samples_and_responses(self):
        print("builds samples and responses:" + '\n')
        # features = [12, 13, 14, 15]
        # dates = ["date1", "date2", "date3"]
        # X = pd.DataFrame(columns=features, index=dates)
        # print(X)
        # X = X.insert(len(X),np.array([1,2,3,4]),True)
        # print(X)
        # print(X)
        # print(X[12])
        X = []
        y = []
        companies_ids = range(1, 10)
        companies_tickers = get_tickers(companies_ids)

        # companies_tickers = ["AVGO","MSFT"]
        # companies_ids = get_companies_ids(companies_tickers)
        # companies_ids = [1, 2, 3, 4, 5, 6, 10]

        start_date = "2010-03-31"
        end_date = "2020-9-30"
        date_str_list = get_quraterly_dates_between(start_date, end_date)

        features_ids = [1, 4, 5, 2, 3, 7]
        features_ids = [1, 2, 3, 5, 7, 8, 9, 10, 11, 12, 16, 17, 18, 19, 20, 21, 22]
        # features_ids = [4, 5]

        print(f"dates are: {start_date} -- {end_date}")
        print(f"companies are: {companies_tickers}")
        print(f"features names are: {get_features_names(features_ids)}")
        print()

        raw_samples = get_samples(companies_ids, date_str_list, features_ids)
        print (f"there are {len(raw_samples)} raw samples")

        resonses = get_responses(companies_ids, date_str_list)

        sample_names = []
        for raw_sample in tqdm(raw_samples, desc='creating X and y from raw samples'):
            if self.is_valid_sample(raw_sample):
                response = get_response_from_responses(resonses, raw_sample.ticker, raw_sample.date_obj)
                if self.is_valid_response(response):
                    # response = self.get_response(raw_sample.ticker, raw_sample.date)
                    X.append(raw_sample.sample)
                    y.append(response)
                    sample_names.append(f"{raw_sample.ticker}({raw_sample.date_obj})")

        print(f"there are {len(sample_names)} valid samples")

        # X_df = pd.DataFrame(X, columns=features_ids, index=cartesian_product_of_dates_and_companies) :TODO add that index
        features_names = get_features_names(features_ids)
        X_df = pd.DataFrame(X, columns=features_names, index=sample_names)
        # y_df = pd.DataFrame(y, index=date_str_list, columns=["Price"]) :TODO add that index
        y_df = pd.DataFrame(y, columns=["Price          "], index=sample_names)
        self.print_samples(X_df, y_df)
        return X_df, y_df

    def print_samples(self, X_df, y_df):

        print("All Samples: ")
        print(X_df.transpose())
        print("All Responses: ")
        print(y_df)

    def is_valid_response(self, response):
        return response is not None and not math.isnan(response)

    @staticmethod
    def get_response(ticker, date):
        date_obj = datetime.datetime.strptime(date, '%Y-%m-%d')
        # while date_obj.weekday() > 4:
        #     date_obj += datetime.timedelta(days=1)
        nbd = next_business_day(date_obj)
        # data = yf.download(ticker, start=date_obj, end=date_obj + datetime.timedelta(days=1), period="1d",
        #                    interval="1d")
        data = yf.download(ticker, start=nbd, end=nbd + datetime.timedelta(days=1))
        return float(data["Open"][0])

    @staticmethod
    def is_valid_sample(raw_sample):
        if None in raw_sample.getSample():
            print(f"bad raw_sample: {raw_sample}")
            return False
        else:
            return True


def get_responses(companies_ids, date_str_list):
    responses = {}
    ticker_list = get_tickers(companies_ids)
    for date_str in tqdm(date_str_list, desc="looping over all given quarters, calling Yahoo on each"):
        date = str_to_date(date_str)
        # nbd = next_business_day(date)
        end_date = date + datetime.timedelta(days=5)
        end_date_str = str(end_date)
        # nbd_str = str(nbd)
        # print(f"is about to download stock info from yahoo for tickers: {ticker_list}, original date: {date_str}, business date: {nbd_str}, looking for range {date_str}-{end_date_str} ")
        print(
            f"is about to download stock info from yahoo for tickers: {ticker_list}, original date: {date_str}, looking for range ({date_str} -- {end_date_str}) ")
        data = yf.download(ticker_list, start=date_str, end=end_date_str, period="1d")
        print(data)
        responses[date] = data
    return responses


def get_response_from_responses(resonses, ticker, date_obj: datetime.date):
    nbd = next_business_day(date_obj)
    try:
        return resonses[date_obj]["Close"][ticker][str(nbd)]
    except:
        print(f"Failed to get response for {ticker} {date_obj} looking for {nbd}")


if __name__ == '__main__':
    dates_list1 = get_quraterly_dates_between("2018-03-31", "2020-06-30")
    print(dates_list1)
