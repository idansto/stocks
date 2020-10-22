import unittest

from sampler.dao.TickersPricesDAO import get_ticker_range


class TestTickerPriceDAO(unittest.TestCase):

    def test_get_ticker_range(self):
        ticker = 'vmw'
        range = get_ticker_range(ticker)
        print(range)
