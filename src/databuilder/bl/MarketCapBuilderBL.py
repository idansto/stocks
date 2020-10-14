import json
import re
from urllib.request import urlopen
from typing import Optional, Any

from tqdm import tqdm

from sampler.dao import CompaniesDAO
from utils.SqlUtils import get_connection_cursor
from utils.StrUtils import getString
from utils.TimerDecorator import timeit

chartData_pattern = re.compile('var chartData = (.+);\\s+var chart =')

def populate_db_market_cap_not_in_db():
    companies_list = get_companies_not_in_market_cap_db()
    populate_db_market_cap(companies=companies_list)


def get_companies_not_in_market_cap_db():
    connection, cursor = get_connection_cursor()
    sql = "select c.ticker from shares.companies c where c.ticker not in (select distinct t.ticker from shares.tickers_prices t where t.market_cap is not NULL)"
    cursor.execute(sql)
    return cursor.fetchall()


def populate_db_market_cap(companies=None):
    companies = companies or CompaniesDAO.get_all_companies()
    connection, cursor = get_connection_cursor()
    for (ticker,) in tqdm(companies):
        populate_single_ticker(connection, cursor, ticker)


@timeit(message=None)
def populate_single_ticker(connection, cursor, ticker):
    json: Optional[Any] = get_json_from_macrotrends(ticker)
    if json:
        my_data = []
        for dict in json:
            date = dict["date"]
            market_cap = dict["v1"]
            t = (date, ticker, market_cap)
            my_data.append(t)

        sql = f"INSERT INTO shares.tickers_prices (date, ticker, market_cap) VALUES (%s, %s, %s) ON DUPLICATE KEY UPDATE market_cap=VALUES(market_cap)"
        cursor.executemany(sql, my_data)
        print(f"there are {len(json)} dates for {ticker}")
        connection.commit()
        print("committed")

        # count = 1
        # for dict in json:
        #     date = dict["date"]
        #     market_cap = dict["v1"]
        #     sql = f"INSERT INTO shares.tickers_prices_fast (date, ticker, market_cap) VALUES ('{date}', '{ticker}', " \
        #           f"{market_cap}) ON DUPLICATE KEY UPDATE market_cap={market_cap}"
        #     # sql = f"INSERT INTO shares.tickers_prices (date, ticker, market_cap) VALUES ('{date}', '{ticker}', " \
        #     #       f"{market_cap})"
        #     cursor.execute(sql)
        #     # if count % 100 == 0:
        #     #     connection.commit()
        #     count += 1
        # print(f"there are {len(json)} dates for {ticker}")
        # connection.commit()
        # print("committed")


@timeit(message="time to get historical data from macrotrends")
def get_json_from_macrotrends(ticker) -> object:
    json_str = get_text_from_macrotrends(ticker)
    if json_str:
        return json.loads(json_str)
    return None


# https://www.macrotrends.net/assets/php/market_cap.php?t=MSFT
def get_text_from_macrotrends(ticker):
    url = f"https://www.macrotrends.net/assets/php/market_cap.php?t={ticker}"
    print(f'url = {url}')
    try:
        connection = urlopen(url)
        html = connection.read()
        # print(f'html = {html}')
        text = getString(html)
        return extract_original_data(text)
    except:
        print(f'failed to read url: {url}')
        return None


def extract_original_data(text: object) -> object:
    match = chartData_pattern.search(text)
    if match:
        found = match.group(1)
        return found
    else:
        print('not found')
        return None


if __name__ == '__main__':
    populate_db_market_cap_not_in_db()