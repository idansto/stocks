import unittest

from sampler.bl.SamplerBL import get_macrotrends_responses_method_b, get_macrotrends_responses, choose_companies, \
    choose_dates
from sampler.dao.CompaniesDAO import get_tickers
from sampler.dao.TickersPricesDAO import get_market_cap, get_market_cap_list
from utils.DateUtils import get_business_date


class TestSamplerBL(unittest.TestCase):

    maxDiff = None

    def test_get_macrotrends_responses_method_b(self):
        result = get_macrotrends_responses_method_b([1, 2], ['2017-03-31', '2018-03-31'])
        print(result)
        self.assertEqual(result, '234234')

    def test_get_macrotrends_responses_methods(self):
        # companies_ids, companies_tickers = choose_companies()
        #
        # companies_ids, companies_tickers = ([1,2], ['AAPL', 'GOOGL', 'GOOG', 'MSFT', 'FB', 'AMZN', 'BRK.B', 'BRK.A', 'BABA', 'JNJ', 'JPM', 'XOM', 'BAC', 'WFC', 'RDS.B', 'WMT', 'RDS.A', 'V', 'CVX', 'PG'])
        companies_ids = range(163, 173)
        # companies_tickers = get_tickers(companies_ids)
        date_str_list = choose_dates()
        # date_str_list = ['2018-03-31']
        macrotrends_responses_a = get_macrotrends_responses(companies_ids, date_str_list)
        macrotrends_responses_b = get_macrotrends_responses_method_b(companies_ids, date_str_list)
        self.assertEqual(macrotrends_responses_a, macrotrends_responses_b)

    def test_get_market_cap(self):
        date, ticker = '2017-06-30', 'FOXA'
        price = get_market_cap(date, ticker)
        print(price)


    def test_business_day(self):
        business_day = get_business_date('2017-06-30')
        print(business_day)

    def test_get_market_cap_list(self):
        market_caps = get_market_cap_list('2017-06-30', get_business_date('2017-06-30'), ['FOXA'])
        print(market_caps)


if __name__ == '__main__':
    unittest.main()
