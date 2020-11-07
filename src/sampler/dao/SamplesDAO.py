from sampler.dao.CompaniesDAO import company_attributes_map
from src.sampler.dto.RawSample import RawSample
from src.utils.SqlUtils import get_connection_cursor
from tqdm import tqdm
import functools

from utils.DateUtils import str_to_date
from utils.StrUtils import create_comma_sperated_list
from utils.TimerDecorator import timeit

COMPANY_ID = 0
TICKER = 1
DATE = 2
SAMPLE_START = 3


# select t.id, t.ticker, t.date,
# t.global_feature1, t.global_feature2, t.feature1, t.feature3, t.feature7, t.feature12, t.feature16, t.feature19 from
# (SELECT c.id, c.ticker,
# (select g.global_metric_value from shares.global_data g where g.global_metric_id = 1 and
# g.date >= dates.date and g.date < date_add(dates.date,INTERVAL 5 DAY) ORDER BY date ASC LIMIT 1) as global_feature1,
# (select g.global_metric_value from shares.global_data g where g.global_metric_id = 2 and
# g.date >= dates.date and g.date < date_add(dates.date,INTERVAL 5 DAY) ORDER BY date ASC LIMIT 1) as global_feature2,
# dates.date,
# (select d.value from shares.feature_data d where d.company_id = c.id and d.date = dates.date and d.feature_id = 1) as feature1,
# (select d.value from shares.feature_data d where d.company_id = c.id and d.date = dates.date and d.feature_id = 3) as feature3,
# (select d.value from shares.feature_data d where d.company_id = c.id and d.date = dates.date and d.feature_id = 7) as feature7,
# (select d.value from shares.feature_data d where d.company_id = c.id and d.date = dates.date and d.feature_id = 12) as feature12,
# (select d.value from shares.feature_data d where d.company_id = c.id and d.date = dates.date and d.feature_id = 16) as feature16,
# (select d.value from shares.feature_data d where d.company_id = c.id and d.date = dates.date and d.feature_id = 19) as feature19 from
# shares.companies c,
# (select '2014-09-30' as date union all select '2014-12-31' as date union all select '2015-03-31' as date union all
# select '2015-06-30' as date union all select '2015-09-30' as date union all select '2015-12-31' as date union all
# select '2016-03-31' as date union all select '2016-06-30' as date union all select '2016-09-30' as date union all
# select '2016-12-31' as date union all select '2017-03-31' as date union all select '2017-06-30' as date union all
# select '2017-09-30' as date union all select '2017-12-31' as date union all select '2018-03-31' as date union all
# select '2018-06-30' as date union all select '2018-09-30' as date union all select '2018-12-31' as date union all
# select '2019-03-31' as date union all select '2019-06-30' as date union all select '2019-09-30' as date union all
# select '2019-12-31' as date union all select '2020-03-31' as date union all select '2020-06-30' as date union all
# select '2020-09-30' as date) as dates
# where c.id in
# (1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50,
# 51,52,53,54,55,56,57,58,59,60,61,62,63,64,65,66,67,68,69,70,71,72,73,74,75,76,77,78,79,80,81,82,83,84,85,86,87,88,89,90,91,92,93,94,95,96,97,98,99,100,
# 101,102,103,104,105,106,107,108,109,110,111,112,113,114,115,116,117,118,119,120,121,122,123,124,125,126,127,128,129,130,131,132,133,134,135,136,137,138,139,140,141,142,143,144,145,146,147,148,149,150,
# 151,152,153,154,155,156,157,158,159,160,161,162,163,164,165,166,167,168,169,170,171,172,173,174,175,176,177,178,179,180,181,182,183,184,185,186,187,188,189,190,191,192,193,194,195,196,197,198,199,200)) as t
# where t.feature1 is not null ORDER by date ASC;
@timeit(message=None)
def get_samples_list_with_all(company_ids, date_list, global_metrics_ids, company_attributes_ids, company_metrics_ids):
    connection, cursor = get_connection_cursor()
    sql = get_samples_sql_with_all(company_ids, date_list, global_metrics_ids, company_attributes_ids,
                                   company_metrics_ids)
    print(sql)
    cursor.execute(sql)

    sample_wrapper_list = []
    for row in tqdm(cursor, colour="CYAN"):
        row_list = list(row)
        company_id = row_list[COMPANY_ID]
        ticker = row_list[TICKER]
        date = row_list[DATE]
        sample = row_list[SAMPLE_START:]
        sample_wrapper = RawSample(company_id, ticker, date, sample)
        sample_wrapper_list.append(sample_wrapper)
    return sample_wrapper_list


def get_samples_with_abs_features(company_ids, date_list, abs_features_ids, features_ids):
    connection, cursor = get_connection_cursor()
    sql = get_samples_sql_with_abs_features(company_ids, date_list, abs_features_ids, features_ids)
    print(sql)
    cursor.execute(sql)

    sample_wrapper_list = []
    for row in tqdm(cursor):
        row_list = list(row)
        company_id = row_list[COMPANY_ID]
        ticker = row_list[TICKER]
        date = row_list[DATE]
        sample = row_list[SAMPLE_START:]
        sample_wrapper = RawSample(company_id, ticker, date, sample)
        sample_wrapper_list.append(sample_wrapper)
    return sample_wrapper_list


@timeit(message=None)
def get_samples(company_ids, date_list, features_ids):
    connection, cursor = get_connection_cursor()
    sql = get_samples_sql(company_ids, date_list, features_ids)
    cursor.execute(sql)

    sample_wrapper_list = []
    for row in tqdm(cursor):
        row_list = list(row)
        company_id = row_list[COMPANY_ID]
        ticker = row_list[TICKER]
        date = row_list[DATE]
        date_obj = str_to_date(date)
        sample = row_list[SAMPLE_START:]
        sample_wrapper = RawSample(company_id, ticker, date_obj, sample)
        sample_wrapper_list.append(sample_wrapper)

    print(f"there are potential {len(sample_wrapper_list)} raw samples")
    return sample_wrapper_list


# [1,2] -> "t.feature1, t.feature2"
def create_small_features_select_list(features_ids):
    return ', '.join(map(id_to_feature_id, features_ids))


def id_to_feature_id(id):
    # return f"IFNULL(t.feature{id}, 0) as feature{id}"
    return "t.feature{}".format(id)


def create_small_global_features_select_list(global_features_ids):
    global_feature_element = map(functools.partial(id_to_key_id, key='global_feature'), global_features_ids)
    return ', '.join(global_feature_element)


def id_to_key_id(id, key):
    return f"t.{key}{id}"


def get_samples_sql_with_all(company_ids, date_list, global_metrics_ids, company_attributes_ids, company_metrics_ids):
    companies = create_comma_sperated_list(company_ids)
    dates = create_dates_table(date_list)

    if len(global_metrics_ids) > 0:
        small_global_metrics = create_small_global_features_select_list(global_metrics_ids) + ', '
        global_metrics = create_golbal_features_select_list(global_metrics_ids) + ', '
    else:
        small_global_metrics = ''
        global_metrics = ''

    if len(company_attributes_ids) > 0:
        t_company_attributes = create_abs_features(company_attributes_ids, 't') + ', '
        c_company_attributes = create_abs_features(company_attributes_ids, 'c') + ', '
    else:
        t_company_attributes = ''
        c_company_attributes = ''

    sql_company_metrics_ids = create_features_select_list(company_metrics_ids)
    small_features = create_small_features_select_list(company_metrics_ids)
    first_feature = id_to_feature_id(company_metrics_ids[0])
    sql = f"select t.id, t.ticker, t.date, {small_global_metrics} {t_company_attributes} {small_features} from " \
          f"(SELECT c.id, c.ticker, {global_metrics} {c_company_attributes} dates.date, {sql_company_metrics_ids} from shares.companies c, " \
          f"({dates}) as dates where c.id in ({companies})) as t where {first_feature} is not null ORDER by date ASC;"
    return sql


def get_samples_sql_with_abs_features(company_ids, date_list, abs_features_ids, features_ids):
    small_features = create_small_features_select_list(features_ids)
    dates = create_dates_table(date_list)
    t_abs_features = create_abs_features(abs_features_ids, 't')
    c_abs_features = create_abs_features(abs_features_ids, 'c')
    features = create_features_select_list(features_ids)
    companies = create_comma_sperated_list(company_ids)
    first_feature = id_to_feature_id(features_ids[0])
    sql = f"select t.id, t.ticker, t.date, {t_abs_features}, {small_features} from (SELECT c.id, c.ticker, {c_abs_features}, dates.date, {features} from shares.companies c, " \
          f"({dates}) as dates where c.id in ({companies})) as t where {first_feature} is not null;"
    return sql


def get_samples_sql(company_ids, date_list, features_ids):
    small_features = create_small_features_select_list(features_ids)
    dates = create_dates_table(date_list)
    features = create_features_select_list(features_ids)
    companies = create_comma_sperated_list(company_ids)
    first_feature = id_to_feature_id(features_ids[0])
    sql = "select t.id, t.ticker, t.date, {} from (SELECT c.id, c.ticker, dates.date, {} from shares.companies c, " \
          "({}) as dates where c.id in ({})) as t where {} is not null;".format(small_features, features, dates,
                                                                                companies, first_feature)
    # print(f"sql is: {sql}")
    return sql


def create_dates_table(date_list):
    dates_with_select_as_date = map(add_select_as_date, date_list)
    union_all = ' union all '.join(dates_with_select_as_date)
    return union_all


def create_abs_features(abs_features_ids, char):
    list_of_abs_features = map(functools.partial(create_abs_feature, char=char), abs_features_ids)
    return ',\n'.join(list_of_abs_features)


# IFNULL(t.feature2,0) as feature2
def create_abs_feature(abs_feature_id, char):
    # return f"IFNULL({char}.{abs_features_map[abs_feature_id]}, 0) as {abs_features_map[abs_feature_id]}"
    return f"{char}.{company_attributes_map[abs_feature_id]}"


def add_select_as_date(date):
    return "select '{}' as date".format(date)


def create_features_select_list(features_ids):
    list_of_features = map(create_feature, features_ids)
    return ',\n'.join(list_of_features)


def create_feature(feature_id):
    return "(select d.value from shares.feature_data d where d.company_id = c.id and d.date = dates.date and " \
           "d.feature_id = {}) as feature{}".format(
        feature_id, feature_id)


def create_golbal_features_select_list(global_features_ids):
    list_of_global_features = map(create_global_feature, global_features_ids)
    return ',\n'.join(list_of_global_features)


def create_global_feature(global_feature_id):
    # return f"(select g.global_metric_value from shares.global_data g where g.global_metric_id = " \
    #        f"{global_feature_id} and g.date >= dates.date and g.date < date_add(dates.date,INTERVAL 5 DAY) " \
    #        f"ORDER BY date ASC LIMIT 1) as global_feature{global_feature_id}"
    #
    # SELECT g.global_metric_value FROM
    # shares.global_data
    # g
    # where
    # global_metric_id = 2 and (date = '2018-06-30' or date = date_add('2018-06-30', INTERVAL 1 DAY) or date = date_add(
    #     '2018-06-30', INTERVAL 2 DAY) or date = date_add('2018-06-30', INTERVAL 3 DAY))
    #     limit 1;
    # SELECT
    # g.global_metric_value
    # FROM
    # shares.global_data
    # g
    # inner
    # join
    # business_days
    # b
    # on
    # g.date = b.business_day
    # where
    # b.date = '2018-06-30' and global_metric_id = 2

    return f"(SELECT g.global_metric_value from shares.global_data g INNER JOIN business_days b " \
           f"ON (g.date = b.business_day) WHERE b.date = dates.date AND global_metric_id = {global_feature_id}) " \
           f"as global_feature{global_feature_id}"


    # return f"(select g.global_metric_value from shares.global_data g where g.global_metric_id = {global_feature_id} and " \
    #        f"(date = dates.date or date = date_add(dates.date, INTERVAL 1 DAY) " \
    #        f"or date = date_add(dates.date, INTERVAL 2 DAY) or date = date_add(dates.date, INTERVAL 3 DAY)) limit 1) " \
    #        f"as global_feature{global_feature_id}"

    # return f"(select g.global_metric_value from shares.global_data g where g.global_metric_id = " \
    #        f"{global_feature_id} and g.date = dates.date) as global_feature{global_feature_id}"
