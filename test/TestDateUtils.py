import datetime
import unittest
from datetime import timedelta

from utils.Colors import bcolors
from utils.DateUtils import next_business_day, str_to_date, get_quraterly_dates_between


class TestDateUtils(unittest.TestCase):

    def test_next_business_day(self):
        date_str = '2016-12-31'
        current_date = str_to_date(date_str)
        next_day = next_business_day(current_date)
        print(next_day)

    def test_get_quraterly_dates_between(self):
        start_date_str = "2020-03-31"
        end_date_str = "2020-9-30"
        date_str_list = get_quraterly_dates_between(start_date_str, end_date_str)
        print(date_str_list)

    def test_adding_dates(self):
        date = str_to_date('2020-03-31')
        next_date = date + datetime.timedelta(days=91)
        print(f"next date = {next_date}")

    def test_color_printing(self):
        print(f"{bcolors.OKBLUE}Warning: No active frommets remain. Continue?{bcolors.ENDC}")

