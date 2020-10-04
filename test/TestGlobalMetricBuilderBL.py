import unittest

from databuilder.bl.GlobalMetricBuilderBL import populate_federal_funds_rate_from_json, populate_federal_funds_rate_TRY, \
    populate_10_year_treasury_rate_from_json, test_insert1


class TestGlobalMetricBuilderBl(unittest.TestCase):

    def test_populate_federal_funds_rate_from_json(self):
        populate_federal_funds_rate_from_json()

    def test_populate_10_year_treasury_rate_from_json(self):
        populate_10_year_treasury_rate_from_json()

    def test_test_insert1(self):
        test_insert1()

############################################################

# def test_populate_federal_funds_rate(self):
#     populate_federal_funds_rate_TRY()

