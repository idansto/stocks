from csv import reader

from utils.sqlUtils import getConnectionCursor


def populate_global_metric_data():
    pass

def populate_Federal_Funds_Rate():
    # (connection, cursor) = getConnectionCursor()
    with open('/resources/fed-funds-rate-historical-chart.csv', 'r') as file:
        csv_reader = reader(file)
        for row in csv_reader:
            (date, value) = row
            sql = "insert (date, metric_name, value) into shares.global_data values (%s, %s, %s)"
            values = (date, 1, value)
            print(sql, values)
    #         cursor.execute(sql)
    # connection.commit()