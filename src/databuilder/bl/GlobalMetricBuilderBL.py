from csv import reader

from sampler.dao.GlobalMetricDAO import get_max_date_for_metric_id
from utils.DateUtils import str_to_date


def populate_global_metric_data():
    pass


def read_till_data(csv_reader):
    for row in csv_reader:
        size_of_line = len(row)
        if size_of_line == 2:
            (date, value) = row
            if date.strip() == 'date' and value.strip() == 'value':
                return


def read_thru_date(csv_reader, latest_date):
    for row in csv_reader:
        (date_str, value) = row
        date = str_to_date(date_str)
        if (date > latest_date):
            return row


def populate_federal_funds_rate_from_json():
    # (connection, cursor) = get_connection_cursor()
    with open('../resources/fed-funds-rate-historical-chart.csv', 'r') as file:
        csv_reader = reader(file)
        read_till_data(csv_reader)
        latest_date = get_max_date_for_metric_id(1)
        first_new_row = read_thru_date(csv_reader, latest_date)
        insert_row_to_global_data(first_new_row)
        for row in csv_reader:
            insert_row_to_global_data(row)
    # connection.commit
    return


def insert_row_to_global_data(row):
    (date, value) = row
    sql = "insert (date, metric_name, value) into shares.global_data values (%s, %s, %s)"
    values = (date, 1, value)
    print(sql, values)
    # cursor.execute(sql)
