import unittest
import yfinance as yf
import datetime


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


if __name__ == '__main__':
    unittest.main()
