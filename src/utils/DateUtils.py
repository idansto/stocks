import datetime
import re
import pandas_market_calendars as mcal


date_pattern = re.compile("^\d{4}-\d{1,2}-\d{1,2}$")

def is_date(key):
    result = date_pattern.match(key)
    # print(key, pattern, result)
    return result


def str_to_date(date_str):
    return datetime.datetime.strptime(date_str, '%Y-%m-%d').date()

def next_business_day(date):
    nyse = mcal.get_calendar('NYSE')
    end_date = date + datetime.timedelta(days=5)
    first_business_date_str = nyse.valid_days(start_date=date, end_date=end_date)[0]
    busienss_day = first_business_date_str.to_pydatetime().date()
    return busienss_day
