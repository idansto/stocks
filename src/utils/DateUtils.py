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


def next_quarter_date_after(date):
    date_components_list = date.split(sep='-')
    year = int(date_components_list[0])
    month = int(date_components_list[1])
    day = int(date_components_list[2])

    if month == 3:
        # return str(year) + '-06-30'
        return f"{year}-06-30"
    if month == 6:
        return str(year) + '-09-30'
    if month == 9:
        return str(year) + '-12-31'
    if month == 12:
        return str(year + 1) + '-03-31'


def get_quraterly_dates_between(start_date, end_date):  # TODO

    # start_year = int(start_date.split(sep='-')[0])
    # start_month = int(start_date.split(sep='-')[1])
    # start_day = int(start_date.split(sep='-')[2])
    #
    # end_year = int(start_date.split(sep='-')[0])
    # end_month = int(start_date.split(sep='-')[1])
    # end_day = int(start_date.split(sep='-')[2])

    dates_list = []

    dates_list.append(start_date)
    current_date = start_date
    next_quarter_date_str = next_quarter_date_after(current_date)
    while next_quarter_date_str <= end_date:
        # next_quarter_date = str_to_date(next_quarter_date_str)
        dates_list.append(next_quarter_date_str)
        next_quarter_date_str = next_quarter_date_after(next_quarter_date_str)

    return dates_list