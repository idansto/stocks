import unittest

from databuilder.bl.GlobalMetricBuilderBL import populate_federal_funds_rate_from_json, populate_federal_funds_rate_TRY, \
    populate_10_year_treasury_rate_from_json, populate_10_Year_Treasury_Rate


class TestGlobalMetricBuilderBl(unittest.TestCase):

    def test_populate_federal_funds_rate_from_json(self):
        populate_federal_funds_rate_from_json()

    def test_populate_10_year_treasury_rate_from_json(self):
        populate_10_year_treasury_rate_from_json()

    def test_populate_10_year_treasury_rate(self):
        populate_10_Year_Treasury_Rate()


############################################################

# def test_populate_federal_funds_rate(self):
#     populate_federal_funds_rate_TRY()

