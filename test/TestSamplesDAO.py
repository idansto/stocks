import unittest

from sampler.dao.SamplesDAO import create_dates_table, create_features_select_list, create_companies, \
    create_small_features_select_list, getSamplesSql, get_samples, get_samples_with_abs_features, get_samples_with_all


class TestDAO(unittest.TestCase):

    def test_create_dates_table(self):
        dates = create_dates_table(["2020-3-31","2020-6-30"])
        self.assertEqual(dates, "select '2020-3-31' as date union all select '2020-6-30' as date")

    def test_create_features_list(self):
        features = create_features_select_list([1, 2, 3])
        self.assertEqual(features, "(select d.value from shares.feature_data d where d.company_id = c.id and d.date = dates.date and d.feature_id = 1) as feature1,\n"+
                                   "(select d.value from shares.feature_data d where d.company_id = c.id and d.date = dates.date and d.feature_id = 2) as feature2,\n"+
                                   "(select d.value from shares.feature_data d where d.company_id = c.id and d.date = dates.date and d.feature_id = 3) as feature3")

    def test_create_companies(self):
        companies = create_companies([1,2,3])
        self.assertEqual(companies, "1,2,3")
        print(companies)

    def test_create_small_features_select_list(self):
        small_features = create_small_features_select_list([1,2])
        self.assertEqual(small_features, "t.feature1, t.feature2")

    def test_getSamplesSql(self):
        sql = getSamplesSql([1,2,3], [4,5], ["2020-3-31","2020-6-30"])
        print(sql)

    def test_get_samples(self):
        sampleList = get_samples([1,2], ["2020-3-31","2020-6-30"], [3,4])
        self.assertEqual("[company_id = 1, ticker = AAPL, date = 2020-3-31, sample = [22370.0, 4565.0], company_id = 2, ticker = GOOGL, date = 2020-3-31, sample = [22177.0, 6820.0], company_id = 1, ticker = AAPL, date = 2020-6-30, sample = [22680.0, 4758.0], company_id = 2, ticker = GOOGL, date = 2020-6-30, sample = [19744.0, 6875.0]]", str(sampleList))
        print(sampleList)

    def test_get_samples_with_abs_features(self):
        sampleList = get_samples_with_abs_features([1,2], ["2020-3-31","2020-6-30"], [3,4], [1,2,3])
        print(sampleList)
        self.assertEqual("[company_id = 1, ticker = AAPL, date = 2020-3-31, sample = ['Computer and Technology', "
                         "'COMPUTER/OFFICE EQUIP', 58313.0, 35943.0, 22370.0], company_id = 2, ticker = GOOGL, "
                         "date = 2020-3-31, sample = ['Computer and Technology', 'COMPUTER SOFT/SERV', 41159.0, "
                         "18982.0, 22177.0], company_id = 1, ticker = AAPL, date = 2020-6-30, sample = ['Computer and "
                         "Technology', 'COMPUTER/OFFICE EQUIP', 59685.0, 37005.0, 22680.0], company_id = 2, "
                         "ticker = GOOGL, date = 2020-6-30, sample = ['Computer and Technology', 'COMPUTER "
                         "SOFT/SERV', 38297.0, 18553.0, 19744.0]]", str(sampleList))

    def test_get_samples_with_all(self):
        sample_list = get_samples_with_all(company_ids=[1,2], date_list=["2020-3-31","2020-6-30"], global_features_ids=[1,2], abs_features_ids=[3,4], features_ids=[1,2,3])
        print(sample_list)
        self.assertEqual("[company_id = 1, ticker = AAPL, date = 2020-3-31, sample = [0.08, 0.7, 'Computer and "
                         "Technology', 'COMPUTER/OFFICE EQUIP', 58313.0, 35943.0, 22370.0], company_id = 2, "
                         "ticker = GOOGL, date = 2020-3-31, sample = [0.08, 0.7, 'Computer and Technology', "
                         "'COMPUTER SOFT/SERV', 41159.0, 18982.0, 22177.0], company_id = 1, ticker = AAPL, "
                         "date = 2020-6-30, sample = [0.08, 0.66, 'Computer and Technology', 'COMPUTER/OFFICE EQUIP', "
                         "59685.0, 37005.0, 22680.0], company_id = 2, ticker = GOOGL, date = 2020-6-30, "
                         "sample = [0.08, 0.66, 'Computer and Technology', 'COMPUTER SOFT/SERV', 38297.0, 18553.0, "
                         "19744.0]]", str(sample_list))

    def test1(self):
        feature = "sdsdf"
        sql = f"select from {feature}"
        print(sql)

if __name__ == '__main__':
    unittest.main()