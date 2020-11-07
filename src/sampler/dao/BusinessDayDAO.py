from utils import DateUtils
from utils.SqlUtils import get_connection_cursor


def get_business_day(date):
    connection, cursor = get_connection_cursor()
    sql = f"select b.business_day from shares.business_days b where b.date = '{date}')"
    print(f"sql is: {sql}")
    cursor.execute(sql)
    result = cursor.fetchone()
    business_day = None
    if result:
        (business_day,) = result
    return business_day


def fill_business_days(missing_dates):
    connection, cursor = get_connection_cursor()

    my_data = []
    for date in missing_dates:
        business_day = DateUtils.get_business_date(date)
        t = (date, business_day)
        my_data.append(t)

    sql = f"insert into shares.business_days (date, business_day) VALUES (%s, %s)"
    cursor.executemany(sql, my_data)
    connection.commit()


