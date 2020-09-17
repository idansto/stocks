from RawSample import *


class SamplerDao:
    @staticmethod
    def get_samples(companies_ids, start_date, end_date, features_ids):
        samples = []
        sam1 = RawSample("MSFT", "2020-06-30", [150, 34.5])
        sam2 = RawSample("AAPL", "2020-06-30", [140, 20.5])
        sam3 = RawSample("FB", "2020-06-30", [110, 80.5])
        sam4 = RawSample("AMZN", "2020-06-30", [190, 50.5])
        samples.append(sam1)
        samples.append(sam2)
        samples.append(sam3)
        samples.append(sam4)
        return samples
