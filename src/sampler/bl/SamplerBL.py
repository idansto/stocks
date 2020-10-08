import datetime
import math

import pandas as pd
import yfinance as yf
from tqdm import tqdm

from sampler.dao.CompaniesDAO import get_tickers
from sampler.dao.FeaturesDAO import get_features_names
from sampler.dao.TickersPricesDAO import get_closing_price, insert_closing_price, get_missing_tickers
from src.sampler.dao.SamplesDAO import get_samples
from utils.DateUtils import get_quraterly_dates_between, next_business_day, str_to_date
from utils.TimerDecorator import timeit


def choose_companies():
    companies_ids = range(4, 6)
    companies_tickers = get_tickers(companies_ids)
    # companies_tickers = ["AVGO","MSFT"]
    # companies_ids = get_companies_ids(companies_tickers)
    # companies_ids = [1, 2, 3, 4, 5, 6, 10]
    print(f"Chosen {len(companies_tickers)} companies which are: {companies_tickers}")
    return companies_ids, companies_tickers


def choose_dates():
    start_date = "2019-09-30"
    end_date = "2019-09-30"
    date_str_list = get_quraterly_dates_between(start_date, end_date)
    print(f"Dates are: {len(date_str_list)} dates: ({start_date} -- {end_date})")
    return date_str_list


def choose_features():
    features_ids = [1, 4, 5, 2, 3, 7]
    features_ids = [1, 2, 3, 5, 7, 8, 9, 10, 11, 12, 16, 17, 18, 19, 20, 21, 22]
    # features_ids = [4, 5]

    print(f"{len(features_ids)} features, names are: {get_features_names(features_ids)}\n")

    features_names = get_features_names(features_ids)
    return features_ids, features_names


class Sampler:

    @timeit(message=None)
    def build_samples_and_responses(self):
        # choose companies, dates and features
        companies_ids, companies_tickers = choose_companies()
        date_str_list = choose_dates()
        features_ids, features_names = choose_features()

        # get samples
        raw_samples = get_samples(companies_ids, date_str_list, features_ids)
        # valid_raw_samples = [raw_sample for raw_sample in raw_samples if is_valid_sample(raw_sample)]

        # get responses
        responses = get_responses(companies_ids, date_str_list)

        # build X and y
        X, y, sample_names = build_X_and_y(raw_samples, responses)

        # create DataFrame for X and y (samples and results)
        X_df, y_df = build_data_frames(X, features_names, sample_names, y)

        return X_df, y_df


def is_valid_sample(raw_sample):
    if None in raw_sample.getSample():
        print(f"bad raw_sample: {raw_sample}")
        return False
    else:
        return True




@timeit(message=None)
def get_responses(companies_ids, date_str_list):

    date_ticker_to_closing_price_map = {}

    ticker_list = get_tickers(companies_ids)
    for date_str in tqdm(date_str_list, desc="looping over all given quarters, calling Yahoo on each"):

        date = str_to_date(date_str)
        missing_tickers = get_missing_tickers(date, ticker_list)
        sizeof_missing_tickers = len(missing_tickers)

        if sizeof_missing_tickers:
            end_date = date + datetime.timedelta(days=4)
            end_date_str = str(end_date)
            print(f'\nis about to download stock info from yahoo. Original date: {date_str}, looking for range ({date_str} -- {end_date_str}). Looking for {sizeof_missing_tickers} missing tickers: {missing_tickers},  ')
            data = yf.download(missing_tickers, start=date_str, end=end_date_str, period="1d")
            print(data)
            single_date_map = insert_data_into_db(data, missing_tickers, date)
            # responses[date] = data
            date_ticker_to_closing_price_map = {**date_ticker_to_closing_price_map, **single_date_map}

    return date_ticker_to_closing_price_map


def insert_data_into_db(data, missing_tickers, date):
    date_ticker_to_closing_price_map = {}
    nbd = next_business_day(date)
    if len(missing_tickers) == 1:
        ticker = missing_tickers[0]
        closing_price = data["Close"][str(nbd)]
        insert_closing_price(ticker, date, closing_price)
        date_ticker_to_closing_price_map[f"{date}.{ticker}"] = closing_price
    else:
        for ticker in missing_tickers:
            closing_price = data["Close"][ticker][str(nbd)]
            insert_closing_price(ticker, date, closing_price)
            date_ticker_to_closing_price_map[f"{date}.{ticker}"] = closing_price

    return date_ticker_to_closing_price_map


def is_valid_response(response):
    return response is not None and not math.isnan(response)


def get_response_from_responses(responses, ticker, date_obj: datetime.date):
    # nbd = next_business_day(date_obj)
    try:
        # try to get from responses (yahoo)
        # closing_price = responses[date_obj]["Close"][ticker][str(nbd)]
        return responses[f"{date_obj}.{ticker}"]
        # insert_closing_price(ticker, date_obj, closing_price)
    except:
        # try to get from DB
        closing_price = get_closing_price(date_obj, ticker)
        if not closing_price:
            print(f"Failed to get response for {ticker} {date_obj}")

    return closing_price


def print_samples(X_df, y_df):
    print("All Samples: ")
    print(X_df.transpose())
    print("All Responses: ")
    print(y_df)


def build_data_frames(X, features_names, sample_names, y):
    pd.options.display.float_format = '${:,.2f}'.format
    X_df = pd.DataFrame(X, columns=features_names, index=sample_names)
    y_df = pd.DataFrame(y, columns=["Price          "], index=sample_names)
    print_samples(X_df, y_df)
    return X_df, y_df


@timeit(message=None)
def build_X_and_y(valid_raw_samples, responses):
    X = []
    y = []
    sample_names = []
    for raw_sample in tqdm(valid_raw_samples, desc='creating X and y from raw samples'):
        if is_valid_sample(raw_sample):
            response = get_response_from_responses(responses, raw_sample.ticker, raw_sample.date_obj)
            if is_valid_response(response):
                X.append(raw_sample.sample)
                y.append(response)
                sample_names.append(f"{raw_sample.ticker}({raw_sample.date_obj})")

    size_of_valid_samples = len(sample_names)
    size_of_raw_samples = len(valid_raw_samples)
    print(
        f"there are {size_of_valid_samples} valid samples, which are %{size_of_valid_samples / size_of_raw_samples} percent of potential samples")

    return X, y, sample_names


if __name__ == '__main__':
    dates_list1 = get_quraterly_dates_between("2018-03-31", "2020-06-30")
    print(dates_list1)

#############################################################################################

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


# def get_response(ticker, date):
#     date_obj = datetime.datetime.strptime(date, '%Y-%m-%d')
#     nbd = next_business_day(date_obj)
#     data = yf.download(ticker, start=nbd, end=nbd + datetime.timedelta(days=1))
#     return float(data["Open"][0])

