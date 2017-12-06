import pymysql
import json

with open("./configs.json", 'r', encoding='utf-8') as json_file:
    dbconf = json.load(json_file)['db_config']


def query_sql(sql, values):
    try:
        flag = False
        error = {}
        conn = pymysql.connect(host=dbconf['db_host'], port=dbconf['db_port'], user=dbconf['db_username'],
                               passwd=dbconf['db_password'], db=dbconf['db_database'], charset=dbconf['db_charset'])
        with conn.cursor() as cursor:
            cursor.execute(sql, values)
        result = cursor.fetchall()
        # conn.commit()
        print('Sql: ', sql, ' Values: ', values)
    except Exception as err:
        flag = True
        error = err
        print('Error: ', err)
    finally:
        conn.close()
        if flag:
            return {"code": error.args[0], "error": error.args[1]}
    return result


def select(tablename, params={}, fields=[]):
    sql = "select %s from %s " % ('*' if len(fields) == 0 else ','.join(fields), tablename)
    ks = params.keys()
    where = ""
    ps = []
    pvs = []
    if len(ks) > 0:
        for al in ks:
            ps.append(al + " =%s ")
            pvs.append(params[al])
        where += ' where ' + ' and '.join(ps)

    rs = query_sql(sql+where, pvs)
    print('Result: ', rs)
    return rs


# select('member', {'username': 'admin', "status": 1})
