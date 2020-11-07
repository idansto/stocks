from sampler.dao.BusinessDayDAO import fill_business_days
from sampler.dao.GlobalMetricDAO import get_missing_dates


def ensure_business_days(date_str_list):
    missing_dates = get_missing_dates(date_str_list)
    fill_business_days(missing_dates)