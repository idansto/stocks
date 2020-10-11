import datetime
import math

import pandas as pd
import yfinance as yf
from tqdm import tqdm

from sampler.dao import TickersPricesDAO
from sampler.dao.CompaniesDAO import get_tickers
from sampler.dao.FeaturesDAO import get_features_names
from src.sampler.dao.SamplesDAO import get_samples
from utils import DictUtils
from utils.Colors import color
from utils.DateUtils import get_quraterly_dates_between, next_business_day, str_to_date
from utils.TimerDecorator import timeit
from collections import defaultdict


def choose_companies():
    companies_ids = range(1, 20)
    # companies_ids = [3]
    companies_tickers = get_tickers(companies_ids)
    # companies_tickers = ["AVGO","MSFT"]
    # companies_ids = get_companies_ids(companies_tickers)
    # companies_ids = [1, 2, 3, 4, 5, 6, 10]
    print(f"Chosen {len(companies_tickers)} companies which are: {companies_tickers}")
    return companies_ids, companies_tickers


def choose_dates():
    start_date = "2017-09-30"
    end_date = "2020-09-30"
    date_str_list = get_quraterly_dates_between(start_date, end_date)
    print(f"Dates are: {len(date_str_list)} dates: ({start_date} -- {end_date})")
    return date_str_list


def choose_features():
    features_ids = [1, 4, 5, 2, 3, 7]
    # features_ids = [1, 3, 7, 8, 10, 11, 12, 19, 20, 21, 22]
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

        # get samples from DB
        raw_samples = get_samples(companies_ids, date_str_list, features_ids)

        # get responses from Yahoo
        yahoo_responses = get_yahoo_responses(companies_ids, date_str_list)

        # insert new data into DB
        insert_data_into_db(yahoo_responses)

        # build X and y
        X, y, sample_names = build_X_and_y(raw_samples, yahoo_responses, features_names)

        # create DataFrame for X and y (samples and results)
        X_df, y_df = build_data_frames(X, features_names, sample_names, y)

        return X_df, y_df


stat_of_non_valid_features = defaultdict(int)


def is_valid_sample(raw_sample, features_names):
    index = 0
    is_valid = True
    for element in raw_sample.sample:
        if not element:
            current_feature_name = features_names[index]
            stat_of_non_valid_features[current_feature_name] += 1
            is_valid = False
        index += 1

    if not is_valid:
        print(f"bad raw_sample: {raw_sample}")

    return is_valid


@timeit(message=None)
def get_yahoo_responses(companies_ids, date_str_list):
    dateticker_to_closingprice_map = {}

    ticker_list = get_tickers(companies_ids)
    for date_str in tqdm(date_str_list, desc="looping over all given quarters, calling Yahoo on each", colour="CYAN"):

        date = str_to_date(date_str)
        missing_tickers = TickersPricesDAO.get_missing_tickers(date, ticker_list)
        sizeof_missing_tickers = len(missing_tickers)

        if sizeof_missing_tickers:
            end_date = date + datetime.timedelta(days=3)
            end_date_str = str(end_date)
            print(
                f'\nis about to download stock info from yahoo. Original date: {date_str}, looking for range ({date_str} -- {end_date_str}). Looking for {sizeof_missing_tickers} missing tickers: {missing_tickers},  ')
            data = yf.download(missing_tickers, start=date_str, end=end_date_str, period="1d")
            print(data)
            single_date_map = create_dateticker_to_closingprice(data, missing_tickers, date)
            # insert_data_into_db(single_date_map)
            # single_date_map = insert_data_into_db(data, missing_tickers, date)
            # # responses[date] = data
            dateticker_to_closingprice_map = {**dateticker_to_closingprice_map, **single_date_map}

    return dateticker_to_closingprice_map


def create_dateticker_to_closingprice(data, missing_tickers, date):
    map = {}
    nbd = next_business_day(date)
    nbd_str = str(nbd)

    if len(missing_tickers) == 1:
        ticker = missing_tickers[0]
        yahoo_closing_price = DictUtils.safe_get(data, "Close", nbd_str)
        save_converted_closing_price(map, date, ticker, yahoo_closing_price)
    else:
        for ticker in missing_tickers:
            yahoo_closing_price = DictUtils.safe_get(data, "Close", ticker, nbd_str)
            save_converted_closing_price(map, date, ticker, yahoo_closing_price)

    return map


def save_converted_closing_price(map, date, ticker, yahoo_closing_price):
    closing_price = convert_illegal_values_to_negative(yahoo_closing_price)
    map[(date, ticker)] = closing_price


def convert_illegal_values_to_negative(yahoo_closing_price):
    if not yahoo_closing_price:
        return -1
    if math.isnan(yahoo_closing_price):
        return -2
    return yahoo_closing_price


def insert_data_into_db(single_date_map):
    for (date, ticker), closing_price in single_date_map.items():
        TickersPricesDAO.insert_closing_price(ticker, date, closing_price)


def is_valid_response(response):
    return response > 0
    # return response is not None and not math.isnan(response) and not response<0


def get_response_from_yahoo_or_db(yahoo_responses, ticker, date_obj: datetime.date):
    # nbd = next_business_day(date_obj)

    if (date_obj, ticker) in yahoo_responses:
        # try to get from responses (yahoo)
        closing_price = yahoo_responses[(date_obj, ticker)]
    else:
        # try to get from DB
        closing_price = TickersPricesDAO.get_closing_price(date_obj, ticker)
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
def build_X_and_y(raw_samples, yahoo_responses, features_names):
    X = []
    y = []
    sample_names = []

    for raw_sample in tqdm(raw_samples, desc='creating X and y from raw samples', colour="CYAN"):
        if is_valid_sample(raw_sample, features_names):
            response = get_response_from_yahoo_or_db(yahoo_responses, raw_sample.ticker, raw_sample.date_obj)
            if is_valid_response(response):
                X.append(raw_sample.sample)
                y.append(response)
                sample_names.append(f"{raw_sample.ticker}({raw_sample.date_obj})")

    size_of_valid_samples = len(sample_names)
    size_of_raw_samples = len(raw_samples)
    print(
        f"\n{color.BLUE}there are {size_of_valid_samples} valid samples, which are %{(100 * size_of_valid_samples / size_of_raw_samples):2.2f} percent of potential samples{color.END}")
    sorted_non_valid_features = {k: v for k, v in sorted(stat_of_non_valid_features.items(), key=lambda item: item[1])}
    print(f"\n{color.BLUE}Bad features: \n{sorted_non_valid_features}{color.END}")

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

# def insert_data_into_db(data, missing_tickers, date):
#     dateticker_to_closingprice_map = {}
#     nbd = next_business_day(date)
#     if len(missing_tickers) == 1:
#         ticker = missing_tickers[0]
#         closing_price = data["Close"][str(nbd)]
#         TickersPricesDAO.insert_closing_price(ticker, date, closing_price)
#         dateticker_to_closingprice_map[f"{date}.{ticker}"] = closing_price
#     else:
#         for ticker in missing_tickers:
#             closing_price = data["Close"][ticker][str(nbd)]
#             TickersPricesDAO.insert_closing_price(ticker, date, closing_price)
#             dateticker_to_closingprice_map[f"{date}.{ticker}"] = closing_price
#
#     return dateticker_to_closingprice_map

# try:
#     # try to get from responses (yahoo)
#     # closing_price = responses[date_obj]["Close"][ticker][str(nbd)]
#     return yahoo_responses[(date_obj, ticker)]
#     # insert_closing_price(ticker, date_obj, closing_price)
# except:
#     # try to get from DB
#     # closing_price = get_closing_price(date_obj, ticker)
#     closing_price = TickersPricesDAO.get_closing_price(date_obj, ticker)
#     if not closing_price:
#         print(f"Failed to get response for {ticker} {date_obj}")

# def add_single_dateticker_to_closingprice(map, date, ticker, closing_price):
#     if is_valid_response(closing_price):
#         closing_price = -1
#     map[(date,ticker)] = closing_price
