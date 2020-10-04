from csv import reader

from sampler.dao.GlobalMetricDAO import get_max_date_for_metric_id
from utils.DateUtils import str_to_date


def populate_global_metric_data():
    pass


def read_till_data(lines):
    for line in lines:
        splitted_line = date_value_line(line)
        if (splitted_line):
            (date, value) = tuple(splitted_line)
            if date.strip() == 'date' and value.strip() == 'value':
                return


def read_thru_date(lines, latest_date):
    for line in lines:
        splitted_line = line.split(',')
        (date_str, value) = splitted_line
        date = str_to_date(date_str)
        if (date > latest_date):
            return splitted_line


def populate_federal_funds_rate_from_json():
    # (connection, cursor) = get_connection_cursor()
    with open('../resources/fed-funds-rate-historical-chart.csv', 'r') as file:
        lines = iter(file.read().splitlines())
        read_till_data(lines)
        latest_date = get_max_date_for_metric_id(1)
        first_new_line = read_thru_date(lines, latest_date)
        insert_row_to_global_data(first_new_line)
        for line in lines:
            splitted_line = date_value_line(line)
            if (splitted_line):
                insert_row_to_global_data(splitted_line)
    # connection.commit
    return


def insert_row_to_global_data(splitted_line):
    (date_str, value) = splitted_line
    sql = "insert (date, metric_name, value) into shares.global_data values (%s, %s, %s)"
    values = (date_str, 1, value)
    print(sql, values)
    # cursor.execute(sql)

def date_value_line(line):
    splitted_line = line.split(',')
    size_of_line = len(splitted_line)
    if size_of_line == 2:
        return splitted_line
