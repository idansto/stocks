from utils.SqlUtils import get_connection_cursor


def get_last_updated(data_name, ticker, connection=None, cursor=None):
    if not connection:
        connection, cursor = get_connection_cursor()

    sql = f"select t.date from shares.last_updated t where t.data_name ='{data_name}' AND t.ticker = '{ticker}'"
    # print(f"sql is: {sql}")
    cursor.execute(sql)
    result = cursor.fetchone()
    if result:
        (last_updated,) = result
    else:
        last_updated = None
    return last_updated
