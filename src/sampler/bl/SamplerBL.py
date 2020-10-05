import yfinance as yf
import datetime
from src.sampler.dao.SamplesDAO import get_samples
import pandas as pd
from tqdm import tqdm

from utils import DateUtils
from utils.DateUtils import get_quraterly_dates_between


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
        companies_ids = [1, 2, 3, 4, 5, 6, 10]
        start_date = "2012-09-30"
        end_date = "2020-3-30"
        date_list = get_quraterly_dates_between(start_date, end_date)
        features_ids = [1, 4, 5, 2, 3, 7]
        raw_samples = get_samples(companies_ids, date_list, features_ids)

        for raw_sample in tqdm(raw_samples):
            if self.validate_sample(raw_sample):
                response = self.get_response(raw_sample.ticker, raw_sample.date)
                X.append(raw_sample.sample)
                y.append(response)

        # X_df = pd.DataFrame(X, columns=features_ids, index=cartesian_product_of_dates_and_companies) :TODO add that index
        X_df = pd.DataFrame(X, columns=features_ids)
        # y_df = pd.DataFrame(y, index=date_list, columns=["Price"]) :TODO add that index
        y_df = pd.DataFrame(y, columns=["Price"])
        self.print_samples(X_df, y_df)
        return X_df, y_df

    def print_samples(self, X_df, y_df):

        print("All Samples: ")
        print(X_df.transpose())
        print("All Responses: ")
        print(y_df)

    @staticmethod
    def get_response(ticker, date):
        date_obj = datetime.datetime.strptime(date, '%Y-%m-%d')
        # while date_obj.weekday() > 4:
        #     date_obj += datetime.timedelta(days=1)
        next_business_day = DateUtils.next_business_day(date_obj)
        # data = yf.download(ticker, start=date_obj, end=date_obj + datetime.timedelta(days=1), period="1d",
        #                    interval="1d")
        data = yf.download(ticker, start=next_business_day, end=next_business_day + datetime.timedelta(days=1))
        return float(data["Open"][0])

    @staticmethod
    def validate_sample(sample):
        return True


if __name__ == '__main__':
    dates_list1 = get_quraterly_dates_between("2018-03-31", "2020-06-30")
    print(dates_list1)
