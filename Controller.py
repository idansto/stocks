from SamplerFactory import *
from DataBuilder import *
from StocksLearner import *
from StocksLearnerFactory import *


class Controller:
    samples_builder = None
    data_builder = None
    stocks_learner = None

    def get_data(self, dataType):
        self.data_builder = DataBuilder()  # TODO: does the controller needs to build data or not?

    def get_samples(self, samples_type, source="mySQL"):
        self.samples_builder = Sampler(samples_type)
        return self.samples_builder.get_samples_and_responses(source)

    def set_learner(self):
        # self.learner = MLPRegressor(random_state=1, max_iter=10000)

        self.stocks_learner = StocksLearner()

    def get_stocks_list(self):
        return {"AAPL": "apple", "MSFT": "microsoft"}

    def get_samples_type(self):
        return 1

    def get_stocks_learner_type(self):
        return 1

    def run(self):
        samples_type = self.get_samples_type()
        sampler = SamplerFactory.get_sampler(samples_type)
        X, y = sampler.get_samples_and_responses()

        stocks_learner_type = self.get_stocks_learner_type()
        stocks_learner = StocksLearnerFactory.get_stocks_learner(stocks_learner_type)
        stocks_learner.run(X,y)



if __name__ == '__main__':
    controller = Controller()
    controller.run()
