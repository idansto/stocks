import unittest

from sampler.dao.globalMetricDAO import populate_Federal_Funds_Rate


class TestDAO(unittest.TestCase):

    def test_populate_Federal_Funds_Rate(self):
        result = populate_Federal_Funds_Rate()
        self.assertEqual(result, "t.feature1, t.feature2")


if __name__ == '__main__':
    unittest.main()
