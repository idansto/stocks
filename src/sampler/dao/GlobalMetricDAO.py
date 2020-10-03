from utils.SqlUtils import get_connection_cursor


def get_max_date_for_metric_id(id):
    connection, cursor = get_connection_cursor()
    sql = 'select max(g.date) from shares.global_data g where g.global_metric_id =%s'
    values = [id]
    cursor.execute(sql, values)
    date = cursor.fetchone()
    return date


