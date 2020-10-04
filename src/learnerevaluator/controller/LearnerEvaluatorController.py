from src.sampler.bl.SamplerFactory import *
from src.learner.bl.StocksLearnerFactory import *


class Controller:

    def get_samples_type(self):
        return 1

    def get_stocks_learner_type(self):
        return 1

    def evaluate_learning_method(self, samples_type, stocks_learner_type):
        sampler = SamplerFactory.get_sampler(samples_type)
        X, y = sampler.get_samples_and_responses()

        stocks_learner = StocksLearnerFactory.get_stocks_learner(stocks_learner_type)
        score = stocks_learner.run(X, y)
        return score

    def evaluate_learning_methods(self):
        samples_type = self.get_samples_type()
        stocks_learner_type = self.get_stocks_learner_type()
        score = self.evaluate_learning_method(samples_type, stocks_learner_type)


if __name__ == '__main__':
    controller = Controller()
    controller.evaluate_learning_methods()
