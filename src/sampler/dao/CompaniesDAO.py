from utils.SqlUtils import get_connection_cursor

abs_features_map = {1: "exchange", 2: "zacks_x_ind_desc", 3: "zacks_x_sector_desc", 4: "zacks_m_ind_desc", 5: "emp_cnt"}
reverse_abs_features = {v: k for k, v in abs_features_map.items()}


def get_company_attribute_name(company_attribute_id):
    return abs_features_map[company_attribute_id]


def get_company_attribute_names(company_attribute_ids):
    return list(map(get_company_attribute_name, company_attribute_ids))


def get_company_attribute_id(company_attribute_name):
    return reverse_abs_features[company_attribute_name]


def get_company_attribute_ids(company_attribute_names):
    return list(map(get_company_attribute_id, company_attribute_names))


def get_all_companies():
    connection, cursor = get_connection_cursor()
    sql = "select c.id, c.ticker, c.comp_name from shares.companies c where c.ticker = 'AMZN'"
    sql = "select c.id, c.ticker, c.comp_name from shares.companies c"
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


