import datetime
import math

import pandas as pd
import yfinance as yf
from tqdm import tqdm

from databuilder.bl import MarketCapBuilderBL
from sampler.dao import TickersPricesDAO, LastUpdatedDAO
from sampler.dao.CompaniesDAO import get_tickers, get_company_attribute_names, get_companies_ids
from sampler.dao.ComapnyMetricsDAO import get_company_metrics_names
from sampler.dao.GlobalMetricDAO import get_global_metric_names
from src.sampler.dao.SamplesDAO import get_samples, get_samples_with_abs_features, get_samples_list_with_all
from utils import DictUtils, DateUtils
from utils.Colors import color
from utils.DateUtils import get_quraterly_dates_between, next_business_day, str_to_date, get_business_date
from utils.TimerDecorator import timeit
from collections import defaultdict


def choose_companies():
    companies_ids = range(1, 201)
    # companies_ids = [3]
    companies_tickers = get_tickers(companies_ids)
    # companies_tickers = ["LLY","TMO"]
    # companies_ids = get_companies_ids(companies_tickers)
    # companies_ids = [1, 2, 3, 4, 5, 6, 10]
    print(f"Chosen {len(companies_tickers)} companies which are: {companies_tickers}")
    return companies_ids, companies_tickers


def choose_dates():
    start_date = "2014-09-30"
    end_date = "2020-09-30"
    date_str_list = get_quraterly_dates_between(start_date, end_date)
    print(f"Dates are: {len(date_str_list)} dates: ({start_date} -- {end_date})")
    # date_str_list = ['2020-03-31', '2020-06-30']
    return date_str_list


def choose_company_metrics():
    # company_metrics_ids = [1, 4, 5, 2, 3, 7]
    # company_metrics_ids = list(range(23, 23+6))
    company_metrics_ids = [1, 3, 7, 12, 16, 19]
    # company_metrics_ids = [4, 5]
    company_metrics_names = get_company_metrics_names(company_metrics_ids)

    print(f"{len(company_metrics_ids)} companies_metrics names are: {company_metrics_names}")

    return company_metrics_ids, company_metrics_names


def choose_company_attributes():
    company_attributes_ids = []
    company_attributes_names = get_company_attribute_names(company_attributes_ids)

    print(f"{len(company_attributes_names)} companies attributes names are: {company_attributes_names}")

    return company_attributes_ids, company_attributes_names


def choose_global_metrics():
    global_metrics_ids = [1]
    global_metrics_names = get_global_metric_names(global_metrics_ids)

    print(f"{len(global_metrics_names)} global metrics names are: {global_metrics_names}")

    return global_metrics_ids, global_metrics_names


class Sampler:

    @timeit(message=None)
    def build_samples_and_responses(self):
        # choose companies, dates and features
        companies_ids, companies_tickers = choose_companies()
        date_str_list = choose_dates()
        global_metrics_ids, global_metrics_names = choose_global_metrics()
        company_attributes_ids, company_attributes_names = choose_company_attributes()
        company_metrics_ids, company_metrics_names = choose_company_metrics()

        sample_field_names = global_metrics_names + company_attributes_names + company_metrics_names
        print(f"sample fields: {sample_field_names}")

        # get samples from DB
        raw_samples = get_samples_list_with_all(companies_ids, date_str_list, global_metrics_ids, company_attributes_ids, company_metrics_ids)

        # get responses from macrotrends (market cap)
        # macrotrends_responses = get_macrotrends_responses(companies_ids, date_str_list)
        macrotrends_responses = get_macrotrends_responses_method_b(companies_ids, date_str_list)

        # # get responses from Yahoo
        # yahoo_responses = get_yahoo_responses(companies_ids, date_str_list)

        # # insert new data into DB
        # insert_data_into_db(yahoo_responses)

        # build X and y
        X, y, sample_names = build_X_and_y_macrotrends(raw_samples, macrotrends_responses, sample_field_names)
        # X, y, sample_names = build_X_and_y(raw_samples, yahoo_responses, company_metrics_names)

        # create DataFrame for X and y (samples and results)
        all_sample_fields_name = global_metrics_names + company_attributes_names + company_metrics_names
        X_df, y_df = build_data_frames(X, all_sample_fields_name, sample_names, y)

        return X_df, y_df


stat_of_non_valid_features = defaultdict(int)


def is_valid_sample(raw_sample, features_names):
    index = 0
    is_valid = True
    for element in raw_sample.sample:
        if not element or math.isnan(element) or element<0:
            current_feature_name = features_names[index]
            stat_of_non_valid_features[current_feature_name] += 1
            is_valid = False
        index += 1

    if not is_valid:
        print(f"bad raw_sample: {raw_sample}")

    return is_valid


@timeit(message=None)
def get_macrotrends_responses_method_b(companies_ids, date_str_list) -> object:
    dateticker_to_capprice_map = {}
    for date_str in tqdm(date_str_list, desc="looping over all given dates to get macrotrends responses", colour="CYAN"):
        ticker_list = get_tickers(companies_ids)
        business_day = get_business_date(date_str)
        dateticker_to_capprice_map_for_business_day = TickersPricesDAO.get_market_cap_list(date_str, business_day, ticker_list)
        for ticker in ticker_list:
            market_cap = dateticker_to_capprice_map_for_business_day.get((date_str, ticker))
            if market_cap is None:
                # get last_update
                last_updated = LastUpdatedDAO.get_last_updated("market_cap", ticker)
                if DateUtils.is_after(date_str, last_updated):
                    print(
                        f"market cap value for {ticker} and {date_str} is not up to date. retrieving from macrotrends")
                    MarketCapBuilderBL.populate_single_ticker(ticker=ticker)
                    market_cap = TickersPricesDAO.get_market_cap(date_str, ticker)
            dateticker_to_capprice_map[(date_str,ticker)] = market_cap
    return dateticker_to_capprice_map


@timeit(message=None)
def get_macrotrends_responses(companies_ids, date_str_list):
    dateticker_to_capprice_map = {}
    ticker_list = get_tickers(companies_ids)
    for date_str in tqdm(date_str_list, desc="looping over all given quarters to get macrotrends responses", colour="CYAN"):
        for ticker in ticker_list:
            market_cap = get_market_cap(date_str, ticker)
            dateticker_to_capprice_map[(date_str,ticker)] = market_cap
    return dateticker_to_capprice_map


def get_market_cap_for_business_day(business_day, tickers):
    TickersPricesDAO.get_market_cap_list(business_day, tickers)

def get_market_cap(date_str, ticker):
    market_cap = TickersPricesDAO.get_market_cap(date_str, ticker)
    if market_cap is None:
        # get last_update
        last_updated = LastUpdatedDAO.get_last_updated("market_cap", ticker)
        if DateUtils.is_after(date_str, last_updated):
            print(f"market cap value for {ticker} and {date_str} is not up to date. retrieving from macrotrends")
            MarketCapBuilderBL.populate_single_ticker(ticker=ticker)
            market_cap = TickersPricesDAO.get_market_cap(date_str, ticker)
    return market_cap


def get_market_cap_for_list_of_dates(ticker, list_of_dates):
    date_marketcap_map = TickersPricesDAO.get_market_cap_for_list_of_dates(ticker, list_of_dates)
    if len(date_marketcap_map) < len(list_of_dates):
        # get last_update
        last_updated = LastUpdatedDAO.get_last_updated("market_cap", ticker)
        if DateUtils.is_after(list_of_dates[-1], last_updated):
            print(f"market cap value for {ticker} is not up to date. retrieving from macrotrends")
            MarketCapBuilderBL.populate_single_ticker(ticker=ticker)
            market_cap = TickersPricesDAO.get_market_cap_for_list_of_dates(ticker, list_of_dates)
    return date_marketcap_map


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
    # return response > 0
    return response is not None and not math.isnan(response) and response > 0


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
def build_X_and_y_macrotrends(raw_samples, macrotrends_responses, features_names):
    X = []
    y = []
    sample_names = []

    for raw_sample in tqdm(raw_samples, desc='creating X and y from raw samples', colour="CYAN"):
        if is_valid_sample(raw_sample, features_names):
            response = macrotrends_responses[(raw_sample.date_obj, raw_sample.ticker)]
            if is_valid_response(response):
                X.append(raw_sample.sample)
                y.append(response)
                sample_names.append(f"{raw_sample.ticker}({raw_sample.date_obj})")
            else:
                print(f"not valid response ({response}) for {raw_sample.date_obj}-{raw_sample.ticker}")

    size_of_valid_samples = len(sample_names)
    size_of_raw_samples = len(raw_samples)
    print(
        f"\n{color.BLUE}there are {size_of_valid_samples} valid samples, which are "
        f"%{(100 * size_of_valid_samples / size_of_raw_samples):2.2f} percent of potential samples{color.END}")
    sorted_non_valid_features = {k: v for k, v in sorted(stat_of_non_valid_features.items(), key=lambda item: item[1])}
    print(f"\n{color.BLUE}Bad features: \n{sorted_non_valid_features}{color.END}")

    return X, y, sample_names


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
        f"\n{color.BLUE}there are {size_of_valid_samples} valid samples, which are "
        f"%{(100 * size_of_valid_samples / size_of_raw_samples):2.2f} percent of potential samples{color.END}")
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
