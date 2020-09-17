from SamplerFactory import *
from StocksLearnerFactory import *


class Controller:
    # def get_data(self, dataType):
    #     self.data_builder = DataBuilder()  # TODO: does the controller needs to build data or not?
    #
    # # def get_samples(self, samples_type, source="mySQL"):
    # #     self.samples_builder = Sampler(samples_type)
    # #     return self.samples_builder.get_samples_and_responses(source)

    # def get_stocks_list(self):
    #     return {"AAPL": "apple", "MSFT": "microsoft"}

    def get_samples_type(self):
        return 1

    def get_stocks_learner_type(self):
        return 1

    def evaluate_learning_method(self, samples_type, stocks_learner_type):
        sampler = SamplerFactory.get_sampler(samples_type)
        X, y = sampler.get_samples_and_responses("mySQL")

        stocks_learner = StocksLearnerFactory.get_stocks_learner(stocks_learner_type)
        score = stocks_learner.run(X, y)
        return score

    def evaluate_learning_methods(self):
        samples_type = self.get_samples_type()
        stocks_learner_type = self.get_stocks_learner_type()
        score = self.evaluate_learning_method(samples_type, stocks_learner_type)
        print('Score: ', score)


if __name__ == '__main__':
    controller = Controller()
    controller.evaluate_learning_methods()
