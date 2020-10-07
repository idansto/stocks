# from sklearn.neural_network import MLPRegressor
from sklearn.linear_model import LinearRegression
import pandas as df
from sklearn.model_selection import train_test_split
from sklearn.neural_network import MLPRegressor
from sklearn.neighbors import KNeighborsRegressor

from utils.TimerDecorator import timeit


class StocksLearner:
    learner = MLPRegressor(random_state=1, max_iter=10000)
    # learner = KNeighborsRegressor(n_neighbors=2)
    # learner = LinearRegression()

    print(f"learner type is: {type(learner)}")

    def fit(self, X_train, y_train):
        self.learner.fit(X_train, y_train)

    def predict(self, X):
        return df.DataFrame(self.learner.predict(X), columns=["Predicted Price"], index=X.index)

    def score(self, X_test, y_test):
        return self.learner.score(X_test, y_test)

    def print_result_table(self, ids_list, X_test, y_test, y_prediction):
        print("\nTEST SAMPLES (X_test): ")
        print(X_test.transpose())

        print("\nTEST RESULTS (y_prediction): ")
        print(y_test.transpose().round(2))

        print("\nTEST RESULT PREDCTION (y_prediction): ")
        print(y_prediction.transpose().round(2))

        print('\nACTUAL Vs PREDICTION (y_test vs y_prediction)')
        print(df.concat([y_test, y_prediction], axis=1))

    def split_samples(self, X, y):  # TODO: use sklearn split method.
        # return X[:len(X) // 2], y[:len(y) // 2], X[len(X) // 2:], y[len(y) // 2:]
        # return train_test_split(X, y, test_size = 0.20, random_state = 42)
        return train_test_split(X, y, test_size = 0.20, shuffle=False)


    #@timeit(message="The learning phase")
    def run(self, X, y):
        X_train, X_test, y_train, y_test = self.split_samples(X, y)
        self.fit(X_train, y_train)
        y_prediction = self.predict(X_test)
        score = self.score(X_test, y_test)
        samples_ids_list = range(len(y_test))
        self.print_result_table(samples_ids_list, X_test, y_test, y_prediction)
        print('\n' + "score -->  ", score)
        return score


if __name__ == '__main__':
    pass
