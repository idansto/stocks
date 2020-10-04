from src.sampler.dto.RawSample import RawSample
from src.utils.SqlUtils import get_connection_cursor
from tqdm import tqdm

COMPANY_ID = 0
TICKER = 1
DATE = 2
SAMPLE_START = 3


def get_samples(company_ids, features_ids, date_list):
    connection, cursor = get_connection_cursor()
    sql = getSamplesSql(company_ids, features_ids, date_list)
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


def getSamplesSql(company_ids, features_ids, date_list):
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


def add_select_as_date(date):
    return "select '{}' as date".format(date)


def create_features_select_list(features_ids):
    list_of_features = map(create_feature, features_ids)
    return ',\n'.join(list_of_features)


def create_feature(feature_id):
    return "(select d.value from shares.feature_data d where d.company_id = c.id and d.date = dates.date and d.feature_id = {}) as feature{}".format(
        feature_id, feature_id)


def create_companies(company_ids):
    return ",".join(map(str, company_ids))
