import unittest

from databuilder.bl.GlobalMetricBuilderBL import populate_federal_funds_rate_from_json, populate_federal_funds_rate_TRY, \
    populate_10_year_treasury_rate_from_json, populate_10_Year_Treasury_Rate, populate_fed_funds_rate_historical_chart, \
    populate_1_year_libor_rate_historical_chart, populate_30_year_fixed_mortgage_rate_chart, \
    populate_historical_libor_rates_chart


class TestGlobalMetricBuilderBl(unittest.TestCase):

    def test_populate_federal_funds_rate_from_json(self):
        populate_federal_funds_rate_from_json()

    def test_populate_10_year_treasury_rate_from_json(self):
        populate_10_year_treasury_rate_from_json()

    def test_populate_10_year_treasury_rate(self):
        populate_10_Year_Treasury_Rate()

    def test_populate_fed_funds_rate_historical_chart(self):
        populate_fed_funds_rate_historical_chart()

    def test_populate_1_year_libor_rate_historical_chart(self):
        populate_1_year_libor_rate_historical_chart()

    def test_populate_30_year_fixed_mortgage_rate_chart(self):
        populate_30_year_fixed_mortgage_rate_chart()

    def test_populate_historical_libor_rates_chart(self):
        populate_historical_libor_rates_chart()


############################################################

# def test_populate_federal_funds_rate(self):
#     populate_federal_funds_rate_TRY()

