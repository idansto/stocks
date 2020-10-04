import unittest

from databuilder.bl.GlobalMetricBuilderBL import populate_federal_funds_rate_from_json


class TestGlobalMetricBuilderBl(unittest.TestCase):

    def test_populate_federal_funds_rate_from_json(self):
        populate_federal_funds_rate_from_json()

