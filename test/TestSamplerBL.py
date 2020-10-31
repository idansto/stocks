import unittest

from sampler.bl.SamplerBL import get_macrotrends_responses_method_b


class TestSamplerBL(unittest.TestCase):

    def test_get_macrotrends_responses_method_b(self):
        result = get_macrotrends_responses_method_b([1, 2], ['2017-03-31', '2018-03-31'])
        print(result)
        self.assertEqual(result, '234234')


if __name__ == '__main__':
    unittest.main()
