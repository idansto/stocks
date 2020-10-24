from utils.SqlUtils import get_connection_cursor


def get_last_updated(data_name, connection=None, cursor=None):
    if not connection:
        connection, cursor = get_connection_cursor()

    sql = f"select t.date from shares.last_updated t where t.data_name ='{data_name}'"
    # print(f"sql is: {sql}")
    cursor.execute(sql)
    (last_updated,) = cursor.fetchone()
    return last_updated
