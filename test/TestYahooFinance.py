import unittest
import yfinance as yf
import datetime

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
        data = yf.download("GOOG", start=next_day, end=next_day + datetime.timedelta(days=1), period="1d", interval="1d",
                   rounding=True)
        self.assertTrue(data['Open'][0], 778.81)

if __name__ == '__main__':
    unittest.main()
