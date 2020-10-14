import unittest

from sampler.dao.CompaniesDAO import get_company_attribute_name, get_company_attribute_names


class TestCompaniesDAO(unittest.TestCase):

    def testConnection(self):
        companies_ids = [1,2,3]
        comp_name_no_brakets = ", ".join(map(str, companies_ids))
        sql = f"select c.id, c.ticker from shares.companies c where c.id in ({comp_name_no_brakets})"
        print(sql)

    def test_get_company_attribute_name(self):
        name = get_company_attribute_name(1)
        print(name)

    def test_get_company_attribute_names(self):
        names = get_company_attribute_names([1,2])
        print(names)



