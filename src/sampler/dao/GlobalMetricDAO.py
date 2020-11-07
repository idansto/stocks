from functools import lru_cache

from sampler.dao.SamplesDAO import create_dates_table
from sampler.dao.TickersPricesDAO import create_dates_sql
from utils.SqlUtils import get_connection_cursor


def get_max_date_for_metric_id(id):
    connection, cursor = get_connection_cursor()
    sql = 'select max(g.date) from shares.global_data g where g.global_metric_id =%s'
    values = [id]
    cursor.execute(sql, values)
    (date, ) = cursor.fetchone()
    return date


def get_global_id():
    pass


def get_global_name():
    pass




def get_global_metric_names(company_attribute_ids):
    return list(map(get_global_metric_name, company_attribute_ids))



def get_global_metric_ids(global_metric_names):
    return list(map(get_global_metric_id, global_metric_names))


@lru_cache(maxsize=1000)
def get_global_metric_id(chart_id, key):
    connection, cursor = get_connection_cursor()
    sql = 'select g.id from shares.global_metrics g where g.chart_id=%s AND g.sub_name=%s'
    values = [chart_id, key]
    cursor.execute(sql, values)
    result = cursor.fetchone()
    if result:
        (id,) = result
    else:
        id = None
    return id


@lru_cache(maxsize=1000)
def get_global_metric_name(id):
    connection, cursor = get_connection_cursor()
    sql = 'select g.name, g.sub_name from shares.global_metrics g where g.id=%s'
    values = [id]
    cursor.execute(sql, values)
    result = cursor.fetchone()
    if result:
        (name,sub_name,) = result
    else:
        id = None
    return f"{name}.{sub_name}"


def get_missing_dates(date_str_list):
    connection, cursor = get_connection_cursor()
    business_dates_sql_table = create_dates_table(date_str_list)
    sql = f'select dates.date from ({business_dates_sql_table}) as dates left join shares.business_days b ' \
          'on (dates.date = b.date) ' \
          'where b.business_day is NULL'
    cursor.execute(sql)
    return [item[0] for item in cursor.fetchall()]





############################################################

# glboal_metric_map = {1: '10 Year Treasury Rate', 2: 'Federal Funds Rate'}
# reverse_glboal_metric_map = {v: k for k, v in glboal_metric_map.items()}


# def get_global_metric_name(global_metric_id):
#     return glboal_metric_map[global_metric_id]


# def get_global_metric_id(global_metric_name):
#     return reverse_glboal_metric_map[global_metric_name]

