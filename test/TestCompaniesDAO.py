import unittest

class TestCompaniesDAO(unittest.TestCase):

    def testConnection(self):
        companies_ids = [1,2,3]
        comp_name_no_brakets = ", ".join(map(str, companies_ids))
        sql = f"select c.id, c.ticker from shares.companies c where c.id in ({comp_name_no_brakets})"
        print(sql)


