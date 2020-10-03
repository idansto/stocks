import unittest
import datetime

from sampler.dao.GlobalMetricDAO import get_max_date_for_metric_id


class TestGlobalMetricDAO(unittest.TestCase):

    def test_get_max_date_for_metric_id(self):
        old_date = datetime.datetime.strptime('2019-3-31','%Y-%m-%d').date()
        (date1,) = get_max_date_for_metric_id(1)
        self.assertTrue(date1 > old_date)