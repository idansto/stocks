from src.sampler.dto.RawSample import RawSample
from src.utils.SqlUtils import get_connection_cursor
from tqdm import tqdm
import functools

COMPANY_ID = 0
TICKER = 1
DATE = 2
SAMPLE_START = 3

abs_features_map = {1: "exchange", 2: "zacks_x_ind_desc", 3: "zacks_x_sector_desc", 4: "zacks_m_ind_desc", 5: "emp_cnt"}


def get_samples_with_all(company_ids, date_list, global_features_ids, abs_features_ids, features_ids):
    connection, cursor = get_connection_cursor()
    sql = getSamplesSql_with_all(company_ids, date_list, global_features_ids, abs_features_ids, features_ids)
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


def get_samples_with_abs_features(company_ids, date_list, abs_features_ids, features_ids):
    connection, cursor = get_connection_cursor()
    sql = getSamplesSql_with_abs_features(company_ids, date_list, abs_features_ids, features_ids)
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
        sample = row_list[SAMPLE_START:]
        sample_wrapper = RawSample(company_id, ticker, date, sample)
        sample_wrapper_list.append(sample_wrapper)
    return sample_wrapper_list


# [1,2] -> "t.feature1, t.feature2"
def create_small_features_select_list(features_ids):
    return ', '.join(map(id_to_feature_id, features_ids))


def id_to_feature_id(id):
    return "t.feature{}".format(id)


def create_small_global_features_select_list(global_features_ids):
    global_feature_element = map(functools.partial(id_to_key_id, key='global_feature'), global_features_ids)
    return ', '.join(global_feature_element)


def id_to_key_id(id, key):
    return f"t.{key}{id}"


def getSamplesSql_with_all(company_ids, date_list, global_features_ids, abs_features_ids, features_ids):
    small_global_features = create_small_global_features_select_list(global_features_ids)
    global_features = create_golbal_features_select_list(global_features_ids)
    small_features = create_small_features_select_list(features_ids)
    dates = create_dates_table(date_list)
    t_abs_features = create_abs_features(abs_features_ids, 't')
    c_abs_features = create_abs_features(abs_features_ids, 'c')
    features = create_features_select_list(features_ids)
    companies = create_companies(company_ids)
    first_feature = id_to_feature_id(features_ids[0])
    sql = f"select t.id, t.ticker, t.date, {small_global_features}, {t_abs_features}, {small_features} from " \
          f"(SELECT c.id, c.ticker, {global_features}, {c_abs_features}, dates.date, {features} from shares.companies c, " \
          f"({dates}) as dates where c.id in ({companies})) as t where {first_feature} is not null;"
    return sql


def getSamplesSql_with_abs_features(company_ids, date_list, abs_features_ids, features_ids):
    small_features = create_small_features_select_list(features_ids)
    dates = create_dates_table(date_list)
    t_abs_features = create_abs_features(abs_features_ids, 't')
    c_abs_features = create_abs_features(abs_features_ids, 'c')
    features = create_features_select_list(features_ids)
    companies = create_companies(company_ids)
    first_feature = id_to_feature_id(features_ids[0])
    sql = f"select t.id, t.ticker, t.date, {t_abs_features}, {small_features} from (SELECT c.id, c.ticker, {c_abs_features}, dates.date, {features} from shares.companies c, " \
          f"({dates}) as dates where c.id in ({companies})) as t where {first_feature} is not null;"
    return sql


def get_samples_sql(company_ids, date_list, features_ids):
    small_features = create_small_features_select_list(features_ids)
    dates = create_dates_table(date_list)
    features = create_features_select_list(features_ids)
    companies = create_companies(company_ids)
    first_feature = id_to_feature_id(features_ids[0])
    sql = "select t.id, t.ticker, t.date, {} from (SELECT c.id, c.ticker, dates.date, {} from shares.companies c, " \
          "({}) as dates where c.id in ({})) as t where {} is not null;".format(small_features, features, dates,
                                                                                companies, first_feature)
    return sql


def create_dates_table(date_list):
    dates_with_select_as_date = map(add_select_as_date, date_list)
    union_all = ' union all '.join(dates_with_select_as_date)
    return union_all


def create_abs_features(abs_features_ids, char):
    list_of_abs_features = map(functools.partial(create_abs_feature, char=char), abs_features_ids)
    return ',\n'.join(list_of_abs_features)


def create_abs_feature(abs_feature_id, char):
    return f"{char}.{abs_features_map[abs_feature_id]}"


def add_select_as_date(date):
    return "select '{}' as date".format(date)


def create_features_select_list(features_ids):
    list_of_features = map(create_feature, features_ids)
    return ',\n'.join(list_of_features)


def create_feature(feature_id):
    return "(select d.value from shares.feature_data d where d.company_id = c.id and d.date = dates.date and " \
           "d.feature_id = {}) as feature{}".format(
        feature_id, feature_id)


def create_companies(company_ids):
    return ",".join(map(str, company_ids))


def create_golbal_features_select_list(global_features_ids):
    list_of_global_features = map(create_global_feature, global_features_ids)
    return ',\n'.join(list_of_global_features)


def create_global_feature(global_feature_id):
    return f"(select g.global_metric_value from shares.global_data g where g.global_metric_id = " \
            f"{global_feature_id} and g.date >= dates.date and g.date < date_add(dates.date,INTERVAL 5 DAY) " \
            f"ORDER BY date ASC LIMIT 1) as global_feature{global_feature_id}"
