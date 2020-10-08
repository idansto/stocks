import math
import unittest
import yfinance as yf
import datetime

from pandas import DataFrame

from utils.DateUtils import str_to_date, next_business_day


class TestYahooFinance(unittest.TestCase):

    def test_something(self):
        # self.assertEqual(True, False)
        date = datetime.date(2018, 3, 31)
        while date.weekday() > 4:
            date += datetime.timedelta(days=1)
        # date = date.strftime("%Y-%m-%d")
        print(date)
        data = yf.download("GOOG", start=date, end=date + datetime.timedelta(days=1), period="1d", interval="1d",
                           rounding=True)
        print("hi" + "\n")
        print(float(data["Open"]))

    def test_next_business_day(self):
        date_str = '2016-12-31'
        current_date = str_to_date(date_str)
        print(current_date)
        print(f'current_date = {current_date}')
        next_day = next_business_day(current_date)
        print(f'next_day = {next_day}')
        data = yf.download("GOOG", start=next_day, end=next_day + datetime.timedelta(days=1), period="1d",
                           interval="1d",
                           rounding=True)
        print(data)
        self.assertTrue(data['Open'][0], 778.81)

    def test_range(self):
        data_true_true_true_true = yf.download("AVGO", start='2019-12-31', end='2020-12-31', period="1d",
                           back_adjust=True, auto_adjust=True, actions=True, progress=True,
                           interval="1d",
                           rounding=True)
        data_false_true_true_true = yf.download("AVGO", start='2019-12-31', end='2020-12-31', period="1d",
                           back_adjust=False, auto_adjust=True, actions=True, progress=True,
                           interval="1d",
                           rounding=True)
        data_false_true_false_true = yf.download("AVGO", start='2019-12-31', end='2020-12-31', period="1d",
                           back_adjust=False, auto_adjust=True, actions=False, progress=True,
                           interval="1d",
                           rounding=True)
        data_true_true_false_true = yf.download("AVGO", start='2019-12-31', end='2020-12-31', period="1d",
                           back_adjust=True, auto_adjust=True, actions=False, progress=True,
                           interval="1d",
                           rounding=True)
        data_false_true_false_false = yf.download("AVGO", start='2019-12-31', end='2020-12-31', period="1d",
                           back_adjust=False, auto_adjust=True, actions=False, progress=False,
                           interval="1d",
                           rounding=True)
        data_false_false_false_false = yf.download("AVGO", start='2019-12-31', end='2020-12-31', period="1d",
                           back_adjust=False, auto_adjust=False, actions=False, progress=False,
                           interval="1d",
                           rounding=True)
        data_true_false_false_false = yf.download("AVGO", start='2019-12-31', end='2020-12-31', period="1d",
                           back_adjust=True, auto_adjust=False, actions=False, progress=False,
                           interval="1d",
                           rounding=True)
        data_true_false_true_false = yf.download("AVGO", start='2019-12-31', end='2020-12-31', period="1d",
                           back_adjust=True, auto_adjust=False, actions=True, progress=False,
                           interval="1d",
                           rounding=True)

        print(data_true_true_true_true)
        print(data_false_true_true_true)
        print(data_false_true_false_true)
        print(data_false_true_false_false)
        print(data_false_false_false_false)
        print(data_true_true_false_true)
        print(data_true_false_false_false)
        print(data_true_false_true_false)

    def test_ticker_list(self):
        ticker_list = ["AVGO","MSFT"]
        # ticker_list = ["MSFT"]
        data = yf.download(ticker_list, start='2016-12-29', end='2017-01-05', period="1d")
        data = yf.download(ticker_list, start='2017-01-04', end='2017-01-05', period="1d")
        print(data)

    def test_nan(self):
        x = float('nan')
        a = "sdf"
        y = None
        print(f"x is nan? {math.isnan(x)}")
        print(f"a is nan? {math.isnan(a)}")
        print(f"y is nan? {math.isnan(y)}")

    def testdownload(self):
        data = yf.download(["FB","MSFT"], start='2019-09-30', end='2019-09-30', period="1d")
        data1 = yf.download(["FB","MSFT"], start='2019-09-30', end='2019-09-30', period="1d")
        pass

if __name__ == '__main__':
    unittest.main()
    DataFrame