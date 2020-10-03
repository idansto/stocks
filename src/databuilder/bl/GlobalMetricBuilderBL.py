from csv import reader


def populate_global_metric_data():
    pass


def read_till_data(csv_reader):
    for row in csv_reader:
        size_of_line = len(row)
        if size_of_line == 2:
            (date, value) = row
            if date.strip() == 'date' and value.strip() == 'value':
                return



def populate_federal_funds_rate_from_json():
    # (connection, cursor) = get_connection_cursor()
    with open('../resources/fed-funds-rate-historical-chart.csv', 'r') as file:
        csv_reader = reader(file)
        read_till_data(csv_reader)
        for row in csv_reader:
            (date, value) = row
            sql = "insert (date, metric_name, value) into shares.global_data values (%s, %s, %s)"
            values = (date, 1, value)
            print(sql, values)
    #         cursor.execute(sql)
    # connection.commit
    return