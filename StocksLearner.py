from sklearn.neural_network import MLPRegressor
from sklearn.linear_model import LinearRegression


class StocksLearner:
    # learner = MLPRegressor(random_state=1, max_iter=10000)

    learner = LinearRegression()

    def fit(self, X_train, y_train):
        self.learner.fit(X_train, y_train)

    def predict(self, X):
        return self.learner.predict(X)

    def score(self, X_test, y_test):
        return self.learner.score(X_test, y_test)

    def print_result_table(self, ids_list, y_true, y_prediction):
        result = [ids_list, y_true, y_prediction]

        print("3. printing result table (: ")
        print()
        print("\t" + str(list(ids_list)))
        print("\t" + str(y_true))
        print("\t" + str(y_prediction))
        print()

    def split_samples(self):
        pass

    def run(self, X, y):
        X_train, y_train, X_test, y_test = self.split_samples(X, y)
        self.fit(X_train, y_train)
        prediction = self.predict(X_test)
        score = self.score(X_test, y_test)
        samples_ids_list = range(y_test)
        self.print_result_table(samples_ids_list, y_test, prediction)
        print("score -->  ", score)

if __name__ == '__main__':
    stocksLearner = StocksLearner()
    stocksLearner.run()
