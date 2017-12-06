import pymysql
import json

with open("./configs.json", 'r', encoding='utf-8') as json_file:
    dbconf = json.load(json_file)['db_config']

conn = pymysql.connect(host=dbconf['db_host'], port=dbconf['db_port'], user=dbconf['db_username'],
                       passwd=dbconf['db_password'], db=dbconf['db_database'], charset=dbconf['db_charset'])


def exec_sql(sql, values):
    try:
        with conn.cursor() as cursor:
            cursor.execute(sql, values)
        result = cursor.fetchall()
        # conn.commit()
    finally:
        conn.close()
    return result


def select(tablename, params={}, fields=[]):
    sql = "select %s from %s " % ('*' if len(fields) == 0 else ','.join(fields), tablename)
    ks = params.keys()
    where = " where "
    ps = []
    pvs = []
    if len(ks) > 0:
        for al in ks:
            ps.append(al + " =%s ")
            pvs.append(params[al])
        where += ' and '.join(ps)

    rs = exec_sql(sql+where, pvs)
    print(len(rs), rs)


select('member', {'username': 'admin', "status": 1})
