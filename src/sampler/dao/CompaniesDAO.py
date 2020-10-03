from utils.SqlUtils import get_connection_cursor


def tickerCompanyNameIteratorTRY():
    connection, cursor = get_connection_cursor()
    sql = "select c.ticker, c.comp_name from shares.companies c"
    cursor.execute(sql)
    return cursor.fetchall()
    # print('cursor = ',cursor)
    # for row in cursor:
    #     print('row = ', row)


def company_iterator():
    connection, cursor = get_connection_cursor()
    sql = "select c.id, c.ticker, c.comp_name from shares.companies c where c.ticker >= 'CLUB'"
    cursor.execute(sql)
    return cursor.fetchall()
    # print('cursor = ',cursor)
    # for row in cursor:
    #     print('row = ', row)