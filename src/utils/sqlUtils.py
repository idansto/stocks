import mysql.connector


def getConnectionCursor():
    connection = mysql.connector.connect(
        host="192.168.1.173",
        user="ariel",
        password="ariel",
        database="shares"
    )
    my_cursor = connection.cursor()
    return connection, my_cursor
