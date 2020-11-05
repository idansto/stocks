import unittest

from sampler.dao.GlobalMetricDAO import get_max_date_for_metric_id, get_global_metric_id
from utils.DateUtils import str_to_date


class TestGlobalMetricDAO(unittest.TestCase):

    def test_get_max_date_for_metric_id(self):
        old_date = str_to_date('2019-3-31')
        max_date = get_max_date_for_metric_id(1)
        self.assertTrue(max_date > old_date)

    def test_get_global_metric_id(self):
        id = get_global_metric_id(2016, 'close')
        self.assertEqual(id, 2)
