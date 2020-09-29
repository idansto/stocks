from csv import reader


def populate_global_metric_data():
    pass

def populate_Federal_Funds_Rate():
    # open file in read mode
    with open('D:\PycharmProjects\pythonProject\stocks\resources\fed-funds-rate-historical-chart.csv', 'r') as file:
        csv_reader = reader(file)
        for row in csv_reader:
            (date, value) = row
            sql = "insert (date, metric_name, value) into shares.global_data values (%s, %s, %s)"
            values = ()