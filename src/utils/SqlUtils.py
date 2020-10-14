import mysql.connector


def get_connection_cursor():
    connection = mysql.connector.connect(
        host="192.168.1.173",
        # host="localhost",
        user="ariel",
        password="ariel",
        database="shares"
    )
    my_cursor = connection.cursor()
    return connection, my_cursor
