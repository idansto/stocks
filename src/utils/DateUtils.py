import datetime
import re

date_pattern = re.compile("^\d{4}-\d{1,2}-\d{1,2}$")

def is_date(key):
    result = date_pattern.match(key)
    # print(key, pattern, result)
    return result


def str_to_date(date_str):
    return datetime.datetime.strptime(date_str, '%Y-%m-%d').date()