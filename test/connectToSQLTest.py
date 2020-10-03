import unittest
import mysql.connector

class TestDAO(unittest.TestCase):

    def testConnection(self):
        mySQLConnection = mysql.connector.connect(host='192.168.1.173', database='shares',
                                                  auth_plugin='mysql_native_password', user='ariel', password='ariel')
        cursor = mySQLConnection.cursor(buffered=True)
        sql = "select count(*) from features f"
        cursor.execute(sql)
        record = cursor.fetchall()
        count = record[0][0]
        self.assertTrue(count > 0)

if __name__ == '__main__':
    unittest.main()
