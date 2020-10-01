import mysql.connector

mySQLConnection = mysql.connector.connect(host='192.168.1.173', database='shares',
                                          auth_plugin='mysql_native_password', user='ariel', password='ariel')
cursor = mySQLConnection.cursor(buffered=True)
sql = "select count(*) from features f"
cursor.execute(sql)
data = cursor.fetchall()
print(data)
