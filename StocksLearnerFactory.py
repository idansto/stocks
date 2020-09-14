from StocksLearner import *


class StocksLearnerFactory:
    @staticmethod
    def get_stocks_learner(get_stocks_learner_type):
        return StocksLearner()
