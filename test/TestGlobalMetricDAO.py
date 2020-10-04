import unittest

from sampler.dao.GlobalMetricDAO import get_max_date_for_metric_id
from utils.DateUtils import str_to_date


class TestGlobalMetricDAO(unittest.TestCase):

    def test_get_max_date_for_metric_id(self):
        old_date = str_to_date('2019-3-31')
        result = get_max_date_for_metric_id(1)
        (date1,) = get_max_date_for_metric_id(1)
        self.assertTrue(date1 > old_date)

