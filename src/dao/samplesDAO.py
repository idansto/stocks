from src.RawSample import RawSample
from src.utils.sqlUtils import getConnectionCursor

COMPANY_ID = 0
DATE = 1
SAMPLE_START = 2


def get_samples(company_ids, features_ids, date_list):
    connection, cursor = getConnectionCursor()
    sql = getSamplesSql(company_ids, features_ids, date_list)
    cursor.execute(sql)

    sample_wrapper_list = []
    for row in cursor:
        row_list = list(row)
        company_id = row_list[COMPANY_ID]
        date = row_list[DATE]
        sample = row_list[SAMPLE_START:]
        sampleWrapper = RawSample(company_id, date, sample)
        sample_wrapper_list.append(sampleWrapper)
    return sample_wrapper_list

    # return cursor.fetchall()


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
    sql = "select t.id, t.date, {} from (SELECT c.id, dates.date, {} from shares.companies c, ({}) as dates where c.id in ({})) as t where {} is not null;".format(
        small_features, features, dates, companies, first_feature)
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
