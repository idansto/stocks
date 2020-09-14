import yfinance
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
import numpy as np
import pandas as pd

if __name__ == '__main__':
    # stocks = yfinance.download(tickers="spy", start="2020-07-02")
    # stocks = stocks["Close"]

    # learner.fit(range(len(stocks.transpose())), stocks)
    # print(learner.predict(range(len(stocks))))
    google = yfinance.Ticker("goog")
    print(google.history(period="15y", interval="3mo"))
    print(yfinance.download("goog",))
    # print(google.info)
