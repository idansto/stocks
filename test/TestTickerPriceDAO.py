import unittest

from sampler.dao import TickersPricesDAO
from sampler.dao.TickersPricesDAO import get_ticker_range


class TestTickerPriceDAO(unittest.TestCase):

    def test_get_ticker_range(self):
        ticker = 'vmw'
        range = get_ticker_range(ticker)
        print(range)

    def test_get_market_cap_list(self):
        result = TickersPricesDAO.get_market_cap_list("2017-4-03", ['GOOG','MSFT'])
        print(result)
