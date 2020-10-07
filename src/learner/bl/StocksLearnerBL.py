# from sklearn.neural_network import MLPRegressor
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.neural_network import MLPRegressor


class StocksLearner:
    learner = MLPRegressor(random_state=1, max_iter=10000)
    # learner = KNeighborsRegressor(n_neighbors=2)
    # learner = LinearRegression()

    print(f"learner type is: {type(learner)}")

    def fit(self, X_train, y_train):
        self.learner.fit(X_train, y_train)

    def predict(self, X):
        return pd.DataFrame(self.learner.predict(X), columns=["Predicted Price"], index=X.index)

    def score(self, X_test, y_test):
        return self.learner.score(X_test, y_test)

    def print_result_table(self, X_test, y_test, y_prediction):
        print("\nTEST SAMPLES (X_test): ")
        print(X_test.transpose())

        print("\nTEST RESULTS (y_test): ")
        print(y_test.transpose().round(2))

        print("\nTEST RESULT PREDCTION (y_prediction): ")
        print(y_prediction.transpose().round(2))

        print('\nACTUAL Vs PREDICTION (y_test vs y_prediction)')
        relative_score, ratio_vector = self.relative_score(y_test, y_prediction)

        ratio_vector_df = pd.DataFrame(ratio_vector)
        table = pd.concat([y_test, y_prediction], axis=1)
        print(table)
        # print(pd.concat([conc, ratio_vector_df], axis=1))
        print(f"\nrelative_score -->  {relative_score*100}%")
        # print('\n' + "relative_score -->  ", relative_score)

    def split_samples(self, X, y):  # TODO: use sklearn split method.
        # return X[:len(X) // 2], y[:len(y) // 2], X[len(X) // 2:], y[len(y) // 2:]
        # return train_test_split(X, y, test_size = 0.20, random_state = 42)
        return train_test_split(X, y, test_size=0.20, shuffle=False)

    # @timeit(message="The learning phase")
    def run(self, X, y):
        X_train, X_test, y_train, y_test = self.split_samples(X, y)
        print("1111111111111111111")
        self.fit(X_train, y_train.values)
        print("2222222222222222222")
        y_prediction = self.predict(X_test)
        print("3333333333333333333")
        score = self.score(X_test, y_test)
        print("4444444444444444444")
        self.print_result_table(X_test, y_test, y_prediction)
        print('\n' + "score          -->  ", score)
        return score


    def relative_score(self, y_test, y_prediction):
        ratios = np.array(y_prediction) / np.array(y_test)
        ones = np.ones(len(y_test))
        result = np.absolute(ratios - ones)
        return result.mean(), result


if __name__ == '__main__':
    pass
