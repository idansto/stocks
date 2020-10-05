from csv import reader
from urllib.request import urlopen

from sampler.dao.GlobalMetricDAO import get_max_date_for_metric_id
from utils.DateUtils import str_to_date
from utils.SqlUtils import get_connection_cursor
from utils.StrUtils import getString


def populate_global_metric_data():
    populate_federal_funds_rate_from_json()
    populate_10_year_treasury_rate_from_json()


def populate_federal_funds_rate_from_json():
    populate_general_metric_data_from_json('fed-funds-rate-historical-chart.csv', 1)

def populate_10_year_treasury_rate_from_json():
    populate_general_metric_data_from_json('10-year-treasury-bond-rate-yield-chart.csv', 2)


def populate_general_metric_data_from_json(resourceName, global_metric_id):
    (connection, cursor) = get_connection_cursor()
    with open('../resources/'+resourceName, 'r') as file:
        lines = iter(file.read().splitlines())
        read_till_data(lines)
        latest_date = get_max_date_for_metric_id(global_metric_id)
        first_new_line = read_thru_date(lines, latest_date)
        if first_new_line:
            insert_row_to_global_data(connection, cursor, first_new_line, global_metric_id)
            for line in lines:
                splitted_line = get_date_value_line(line)
                if (splitted_line):
                    insert_row_to_global_data(connection, cursor, splitted_line, global_metric_id)
    connection.commit()

def read_till_data(lines):
    for line in lines:
        splitted_line = get_date_value_line(line)
        if (splitted_line):
            (date, value) = splitted_line
            if date.strip() == 'date' and value.strip() == 'value':
                return


def read_thru_date(lines, latest_date):
    for line in lines:
        splitted_line = get_date_value_line(line)
        if splitted_line:
            (date_str, value) = splitted_line
            date = str_to_date(date_str)
            if (latest_date == None or date > latest_date):
                return splitted_line


def insert_row_to_global_data(connection, cursor, splitted_line, global_metric_id):
    (date_str, value) = splitted_line
    sql = "insert into shares.global_data (date, global_metric_id, global_metric_value) values (%s, %s, %s)"
    values = [date_str, global_metric_id, value]
    cursor.execute(sql, values)
    print(sql, values)

def get_date_value_line(line):
    splitted_line = line.split(',')
    size_of_line = len(splitted_line)
    if size_of_line == 2:
        return splitted_line


################################################################################################

def populate_federal_funds_rate_TRY():
    text = get_federal_funds_rate_html_from_macrotrends_TRY()
    lines = iter(text.splitlines())
    read_till_data(lines)
    latest_date = get_max_date_for_metric_id(1)
    first_new_line = read_thru_date(lines, latest_date)
    (connection, cursor) = get_connection_cursor()
    insert_row_to_global_data(cursor, 1, first_new_line)
    for line in lines:
        splitted_line = get_date_value_line(line)
        if (splitted_line):
            insert_row_to_global_data(cursor, 1, splitted_line)
# connection.commit


def get_federal_funds_rate_html_from_macrotrends_TRY():
    url = 'https://www.macrotrends.net/2015/fed-funds-rate-historical-chart'
    print(f'url = {url}')
    try:
        connection = urlopen(url)
        html = connection.read()
        # print(f'html = {html}')
        text = getString(html)
        return text
    except:
        print(f'failed to read url: {url}')
        return None
