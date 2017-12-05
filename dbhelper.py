import pymysql
from functools import reduce

conn = pymysql.connect()


def exec_sql(sql, values):
    try:
        with conn.cursor() as cursor:
            cursor.execute(sql, values)
        result = cursor.fetchone()
        # conn.commit()
    finally:
        conn.close()
    return result


def composeWhere(x):
    return


def select(tablename, params = {}, fields = []):
    sql = "select * from %s "
    ks = params.keys()
    if len(ks) > 0:
        where = reduce(fn, ks)