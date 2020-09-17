from Sampler import *


class SamplerFactory:

    @staticmethod
    def get_sampler(sampler_type):
        return Sampler()
