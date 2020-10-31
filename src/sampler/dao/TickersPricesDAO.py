from utils import DateUtils, StrUtils
from utils.SqlUtils import get_connection_cursor
from utils.TimerDecorator import timeit


def get_closing_price(date, ticker):
    connection, cursor = get_connection_cursor()
    sql = f"select t.closing_price from shares.tickers_prices t where t.date = '{date}' and t.ticker = '{ticker}'"
    # print(f"sql is: {sql}")
    cursor.execute(sql)
    (closing_price,) = cursor.fetchone()
    return closing_price


def get_market_cap(date, ticker):
    connection, cursor = get_connection_cursor()
    sql = f"select t.market_cap from shares.tickers_prices t where t.ticker = '{ticker}' and t.date >= '{date}' and " \
          f"t.date < date_add('{date}',INTERVAL 5 DAY) ORDER BY date ASC LIMIT 1;"

    # print(f"sql is: {sql}")
    cursor.execute(sql)
    single_result = cursor.fetchone()
    if single_result:
        (market_cap,) = single_result
        return market_cap
    else:
        return None


def get_market_cap_list(business_day, tickers):
    connection, cursor = get_connection_cursor()
    tickers_list = StrUtils.create_comma_sperated_list(tickers)
    sql = f"select t.date, t.ticker, t.market_cap from shares.tickers_prices t where t.ticker in ({tickers_list})' and t.date = '{business_day}';"
    print(f"sql is: {sql}")
    cursor.execute(sql)
    dateticker_to_capprice_map = {}
    for row in cursor:
        (date, ticker, market_cap) = row
        dateticker_to_capprice_map[(date, ticker)] = market_cap
    return dateticker_to_capprice_map



def get_market_cap_for_list_of_dates(ticker, list_of_dates, connection=None, cursor=None):
    if not connection:
        connection, cursor = get_connection_cursor()

    # (select 1 id, '2019-3-31' date union all select 2 id, '2019-6-30' date)
    original_dates_sql = create_dates_sql(list_of_dates)
    list_of_business_dates = DateUtils.get_business_dates(list_of_dates)
    business_dates_sql = create_dates_sql(list_of_business_dates)

    sql = f"select dates.date original_date, t.date business_day, t.market_cap from {original_dates_sql} as dates, {business_dates_sql} as business_dates, shares.tickers_prices t where t.ticker = '{ticker}' AND dates.id=business_dates.id AND t.date = business_dates.date;"
    cursor.execute(sql)
    return cursor.fetchall()


def create_dates_sql(list_of_dates):
    ' union all '.join(map(create_signle_date, enumerate(list_of_dates)))


def create_signle_date(enumurated_data):
    (id, date) = enumurated_data
    return "select {id} id, '{date}' date"



def insert_closing_price(ticker, date_obj, closing_price):
    connection, cursor = get_connection_cursor()
    sql = f"INSERT INTO shares.tickers_prices (date, ticker, closing_price) VALUES ('{date_obj}', '{ticker}', {closing_price})"
    # print(f"sql is: {sql}")
    cursor.execute(sql)
    connection.commit()


def get_missing_tickers(date, ticker_list):
    connection, cursor = get_connection_cursor()
    ticker_list_table_sql = create_ticker_list_table_sql(ticker_list)
    sql = f"select tickers.ticker from ({ticker_list_table_sql}) as tickers where tickers.ticker not in (select " \
          f"t.ticker from shares.tickers_prices t where t.date = '{date}')"
    # print(f"sql is: {sql}")
    cursor.execute(sql)
    tuples = cursor.fetchall()
    return [i[0] for i in tuples]


# (select 'MSFT' as ticker union all select 'GOOG' as ticker) as tickers
def create_ticker_list_table_sql(ticker_list):
    tickers_with_select_as_ticker = map(add_select_as_date, ticker_list)
    union_all = ' union all '.join(tickers_with_select_as_ticker)
    return union_all


def add_select_as_date(ticker):
    return "select '{}' as ticker".format(ticker)


def get_ticker_range(ticker):
    connection, cursor = get_connection_cursor()
    start_date = get_ticker_first_date(ticker, connection, cursor)
    end_date = get_ticker_last_date(ticker, connection, cursor)
    return start_date,end_date


def get_ticker_first_date(ticker, connection=None, cursor=None):
    if not connection:
        connection, cursor = get_connection_cursor()

    sql = f"select t.date from shares.tickers_prices t where t.ticker ='{ticker}' ORDER BY date ASC LIMIT 1"
    # print(f"sql is: {sql}")
    cursor.execute(sql)
    (start_date,) = cursor.fetchone()
    return start_date


def get_ticker_last_date(ticker, connection=None, cursor=None):
    if not connection:
        connection, cursor = get_connection_cursor()

    sql = f"select t.date from shares.tickers_prices t where t.ticker ='{ticker}' ORDER BY date DESC LIMIT 1"
    # print(f"sql is: {sql}")
    cursor.execute(sql)
    (last_date,) = cursor.fetchone()
    return last_date


