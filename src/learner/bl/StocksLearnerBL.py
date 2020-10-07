# from sklearn.neural_network import MLPRegressor
from sklearn.linear_model import LinearRegression
import pandas as df
from sklearn.model_selection import train_test_split
from sklearn.neural_network import MLPRegressor
from sklearn.neighbors import KNeighborsRegressor
import numpy as np


class StocksLearner:
    learner = MLPRegressor(random_state=1, max_iter=10000)  # 825
    # learner = KNeighborsRegressor(n_neighbors=15) #807
    # learner = LinearRegression()  # 1092

    print(f"learner type is: {type(learner)}")

    def fit(self, X_train, y_train):
        self.learner.fit(X_train, y_train)

    def predict(self, X):
        return df.DataFrame(self.learner.predict(X), columns=["Predicted Price"], index=X.index)

    def official_learner_score(self, X_test, y_test):
        return self.learner.score(X_test, y_test)

    def relative_score(self, y_true, y_prediction):
        ratios = np.array(y_prediction) / np.array(y_true)
        print(ratios)
        ones = np.ones(len(y_true))
        print(ones)
        result = np.absolute(ratios - ones)
        return result.sum()

    def print_result_table(self, X_test, y_true, y_prediction):
        print('\n' + "result table: ")
        print('\n' + "TEST SAMPLES: ")
        print(X_test.transpose())
        print()
        print(y_true.transpose().round(2))
        print()
        print(y_prediction.transpose().round(2))
        # y_true.merge(y_prediction, left_index=True, right_index=True)

        print()
        print('my try')
        print(df.concat([y_true, y_prediction], axis=1))

    def split_samples(self, X, y):
        # return X[:len(X) // 2], y[:len(y) // 2], X[len(X) // 2:], y[len(y) // 2:]
        return train_test_split(X, y, test_size=0.20, random_state=42)

    def run(self, X, y):
        X_train, X_test, y_train, y_test = self.split_samples(X, y)
        self.fit(X_train, y_train)
        y_prediction = self.predict(X_test)
        official_learner_score = self.official_learner_score(X_test, y_test)
        relative_score = self.relative_score(y_test, y_prediction)
        self.print_result_table(X_test, y_test, y_prediction)
        print('\n' + "Official learner score -->  ", official_learner_score)
        print('\n' + "Relative score -->  ", relative_score)
        return official_learner_score, relative_score


if __name__ == '__main__':
    learner = StocksLearner()
    learner.run([[1, 2, 3], [4, 5, 6], [1, 2, 3], [4, 5, 6], [1, 2, 3], [4, 5, 6]], [10, 20, 13, 14, 1511, 56])
    # score = learner.score([15, 10], [10, 10])
    # print(score)
