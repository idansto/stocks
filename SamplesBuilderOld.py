import yfinance
import numpy as np

REVENUES = 0


class SamplesBuilder:

    def build_samples(self, stocks_dict):
        samples = []
        dates = ['2019-03-31', '2019-06-30']
        dates = list(stocks_dict["AAPL"][REVENUES].keys())[2:][:5]  # TODO: the 5 is only for debug
        print(dates)
        features = [REVENUES]

        for ticker, financial_info in stocks_dict.items():
            for date in dates:
                sample = []
                for feature in features:
                    sample.append(float(stocks_dict[ticker][feature][date]))
                samples.append(sample)

        responses = self.get_responses(dates, stocks_dict.keys())

        samples, responses = self.validate_samples_and_responses(samples, responses)
        print("lengths are: ", len(samples), len(responses))
        X_train = samples[:len(samples) // 2]
        print("X_train: ")
        print(X_train)

        X_test = samples[len(samples) // 2:]
        print("X_test: ")
        print(X_test)

        y_train = responses[:len(responses) // 2]
        print("y_train: ")
        print(y_train)

        y_test = responses[len(responses) // 2:]
        print("y_test: ")
        print(y_test)

        # print(stocks_dict)
        return X_train, y_train, X_test, y_test
        # print("2. building samples (: ")
        # return [[5], [10], [15]], [50, 100, 150], [[4], [6]], [40, 60]

    def get_responses(self, dates, tickers):
        prices = []
        for ticker in tickers:
            ticker_obj = yfinance.Ticker(ticker)
            # ticker_history = ticker_obj.history(start=dates[-2], end="2020-12-01", period="10y",interval="3mo")  # TODO: calculate the right "end" date
            ticker_history = yfinance.download(ticker,dates[-2],end="2020-09-07",interval="3mo")
            print(ticker_history)
            open_prices = ticker_history["Open"].dropna()
            print(open_prices)
            # open_prices = open_prices[open_prices and open_prices != 0]
            prices += list(open_prices)
        return prices

    def validate_samples_and_responses(self, samples, responses):

        bad_indices = []
        new_responses = []
        for index, response in enumerate(responses):
            if response != response:
                bad_indices.append(index)
            else:
                new_responses.append(response)

        for idx in reversed(bad_indices):
            del samples[idx]

        return samples, new_responses
