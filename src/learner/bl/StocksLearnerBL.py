import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsRegressor
from sklearn.neural_network import MLPRegressor
from sklearn.preprocessing import StandardScaler

from utils.TimerDecorator import timeit


class StocksLearner:
    learner = MLPRegressor(random_state=1, max_iter=10000)
    # learner = KNeighborsRegressor(n_neighbors=12)
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

        # print("\nTEST RESULTS (y_test): ")
        # print(y_test.transpose().round(2))

        # print("\nTEST RESULT PREDCTION (y_prediction): ")
        # print(y_prediction.transpose().round(2))

        print('\nACTUAL Vs PREDICTION (y_test vs y_prediction)')
        relative_score, ratio_vector = self.relative_score(y_test, y_prediction)

        ratio_vector_df = pd.DataFrame(ratio_vector)
        table = pd.concat([y_test, y_prediction], axis=1)
        print(table)
        print(f"\nrelative_score -->  {relative_score * 100: 2.2f}% mistake relates to ground truth")

    def split_samples(self, X, y):
        # return X[:len(X) // 2], y[:len(y) // 2], X[len(X) // 2:], y[len(y) // 2:]
        # return train_test_split(X, y, test_size = 0.20, random_state = 42)
        return train_test_split(X, y, test_size=0.20, shuffle=False)

    @timeit(message="The learning phase")
    def run(self, X, y):
        X, y = self.preproccess_data(X, y)
        X_train, X_test, y_train, y_test = self.split_samples(X, y)
        self.fit(X_train, y_train.values.ravel())
        y_prediction = self.predict(X_test)
        score = self.score(X_test, y_test)
        self.print_result_table(X_test, y_test, y_prediction)
        print(f"\nscore          -->  {score:1.2f}")
        return score

    def relative_score(self, y_test, y_prediction):
        ratios = np.array(y_prediction) / np.array(y_test)
        ones = np.ones(len(y_test))
        result = np.absolute(ratios - ones)
        return result.mean(), result

    def preproccess_data(self, X, y):
        categorial_columns = ["exchangecho"]
        X = pd.get_dummies(X, columns=categorial_columns)

        sc = StandardScaler()
        sc.fit(X)
        X_processed = sc.transform(X)
        X_processed_df = pd.DataFrame(X_processed, columns=X.columns, index=X.index)
        print(X_processed_df)
        return X_processed_df, y


if __name__ == '__main__':
    learner = StocksLearner()
    x1, y2 = learner.preproccess_data(pd.DataFrame([[1, 2, 3], [4, 5, 6], [7, 8, 9]]), [10, 20, 30])
    print(x1)
    print(y2)
