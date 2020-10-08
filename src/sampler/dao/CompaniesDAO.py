from utils.SqlUtils import get_connection_cursor


def company_iterator():
    connection, cursor = get_connection_cursor()
    sql = "select c.id, c.ticker, c.comp_name from shares.companies c where c.ticker >= 'CLUB'"
    cursor.execute(sql)
    return cursor.fetchall()
    # print('cursor = ',cursor)
    # for row in cursor:
    #     print('row = ', row)


def get_tickers(companies_ids):
    connection, cursor = get_connection_cursor()
    comp_name_no_brakets = ", ".join(map(str, companies_ids))
    sql = f"select c.id, c.ticker from shares.companies c where c.id in ({comp_name_no_brakets})"
    # print(f"sql is: {sql}")
    cursor.execute(sql)
    db_map = {}
    for key, value in cursor:
        db_map[key] = value
    tickers = []
    for id in companies_ids:
        tickers.append(db_map[id])
    return tickers


def get_companies_ids(tickers):
    connection, cursor = get_connection_cursor()
    tickers_no_brakets = ", ".join(map(add_quaotes, tickers))
    sql = f"select c.ticker, c.id from shares.companies c where c.ticker in ({tickers_no_brakets})"
    # print(f"sql is: {sql}")
    cursor.execute(sql)
    db_map = {}
    for key, value in cursor:
        db_map[key] = value
    companies_id = []
    for id in tickers:
        companies_id.append(db_map[id])
    return companies_id


def add_quaotes(ticker):
    return f"'{ticker}'"


################################################################################################

def tickerCompanyNameIteratorTRY():
    connection, cursor = get_connection_cursor()
    sql = "select c.ticker, c.comp_name from shares.companies c"
    cursor.execute(sql)
    return cursor.fetchall()
    # print('cursor = ',cursor)
    # for row in cursor:
    #     print('row = ', row)
