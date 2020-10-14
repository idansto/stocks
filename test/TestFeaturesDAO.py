import unittest

from sampler.dao.FeaturesDAO import get_company_metrics_names, get_feature_name


class TestFeaturesDAO(unittest.TestCase):

    def test_get_features_names(self):
        names_list = get_company_metrics_names([1, 2, 3])
        print(names_list)

    def test_get_feature_name(self):
        name = get_feature_name(1)
        print(name)
