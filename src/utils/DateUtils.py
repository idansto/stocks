import re


def is_date(key):
    result = date_pattern.match(key)
    # print(key, pattern, result)
    return result


date_pattern = re.compile("^\d{4}-\d{1,2}-\d{1,2}$")