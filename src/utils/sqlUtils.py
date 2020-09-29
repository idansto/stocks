import mysql.connector


def getConnectionCursor():
    connection = mysql.connector.connect(
        host="localhost",
        user="ariel",
        password="ariel",
        database="shares"
    )
    mycursor = connection.cursor()
    return connection, mycursor