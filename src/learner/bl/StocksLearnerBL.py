# from sklearn.neural_network import MLPRegressor
from sklearn.linear_model import LinearRegression
import pandas as df


class StocksLearner:
    # learner = MLPRegressor(random_state=1, max_iter=10000)

    learner = LinearRegression()

    def fit(self, X_train, y_train):
        self.learner.fit(X_train, y_train)

    def predict(self, X):
        return df.DataFrame(self.learner.predict(X), columns=["Predicted Price"], index=X.index)

    def score(self, X_test, y_test):
        return self.learner.score(X_test, y_test)

    def print_result_table(self, ids_list, X_test, y_true, y_prediction):
        result = [ids_list, y_true, y_prediction]
        print('\n' + "result table: ")
        print('\n' + "TEST SAMPLES: ")
        print(X_test.transpose())
        print()
        print(y_true.transpose())
        print()
        print(y_prediction.transpose())

    def split_samples(self, X, y):  # TODO: use sklearn split method.
        return X[:len(X) // 2], y[:len(y) // 2], X[len(X) // 2:], y[len(y) // 2:]

    def run(self, X, y):
        X_train, y_train, X_test, y_test = self.split_samples(X, y)
        self.fit(X_train, y_train)
        prediction = self.predict(X_test)
        score = self.score(X_test, y_test)
        samples_ids_list = range(len(y_test))
        self.print_result_table(samples_ids_list, X_test, y_test, prediction)
        print('\n' + "score -->  ", score)
        return score


if __name__ == '__main__':
    pass
