import yfinance as yf
import datetime
from sampler.dao.samplesDAO import get_samples
import pandas as pd
from tqdm import tqdm


def next_quarter_date_after(date):
    date_components_list = date.split(sep='-')
    year = int(date_components_list[0])
    month = int(date_components_list[1])
    day = int(date_components_list[2])
    # if day == 30 and (month == 6 or month == 9):
    #     return date
    # if day == 31 and (month == 3 or month == 12):
    #     return date
    if month == 3:
        return str(year) + '-06-30'
    if month == 6:
        return str(year) + '-09-30'
    if month == 9:
        return str(year) + '-12-31'
    if month == 12:
        return str(year + 1) + '-03-31'


def get_dates_between(start_date, end_date):  # TODO

    # start_year = int(start_date.split(sep='-')[0])
    # start_month = int(start_date.split(sep='-')[1])
    # start_day = int(start_date.split(sep='-')[2])
    #
    # end_year = int(start_date.split(sep='-')[0])
    # end_month = int(start_date.split(sep='-')[1])
    # end_day = int(start_date.split(sep='-')[2])

    dates_list = []
    # current_year = start_year
    # current_month = start_month
    # current_day = start_day
    dates_list.append(start_date)
    current_date = start_date
    next_quarter_date = next_quarter_date_after(current_date)
    while next_quarter_date <= end_date:
        dates_list.append(next_quarter_date)
        next_quarter_date = next_quarter_date_after(next_quarter_date)

    return dates_list


class Sampler:
    # sampler_dao = SamplerDao()

    def get_samples_and_responses(self):
        print("builds samples and responses:" + '\n')
        X = []
        y = []
        companies_ids = [2]
        start_date = "2018-12-31"
        end_date = "2019-12-31"
        date_list = get_dates_between(start_date, end_date)
        features_ids = [1, 2]
        # raw_samples = self.sampler_dao.get_samples(companies_ids, start_date, end_date, features_ids)
        raw_samples = get_samples(companies_ids, features_ids, date_list)

        for raw_sample in tqdm(raw_samples):
            # print(raw_sample.date)
            if self.validate_sample(raw_sample):
                response = self.get_response(raw_sample.ticker, raw_sample.date)
                X.append(raw_sample.sample)
                y.append(response)

        self.print_samples(X, y)

        return X, y

    def print_samples(self, X, y):
        X_df = pd.DataFrame(X)
        y_df = pd.DataFrame(y)
        print("samples: ")
        print(X_df.transpose())
        print("responses: ")
        print(y_df)

    @staticmethod
    def get_response(ticker, date):
        date_obj = datetime.datetime.strptime(date, '%Y-%m-%d')
        while date_obj.weekday() > 4:
            date_obj += datetime.timedelta(days=1)
        data = yf.download(ticker, start=date_obj, end=date_obj + datetime.timedelta(days=1), period="1d",
                           interval="1d")
        data = yf.download(ticker, start=date_obj, end=date_obj + datetime.timedelta(days=1))
        return float(data["Open"][0])

    @staticmethod
    def validate_sample(sample):
        return True


if __name__ == '__main__':
    dates_list = get_dates_between("2018-03-31", "2020-06-30")
    print(dates_list)
