import unittest
from datetime import timedelta

from utils.DateUtils import next_business_day, str_to_date


class TestDateUtils(unittest.TestCase):

    def test_next_business_day(self):
        date_str = '2016-12-31'
        current_date = str_to_date(date_str)
        next_day = next_business_day(current_date)
        print(next_day)
