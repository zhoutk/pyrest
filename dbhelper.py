import pymysql
import json

with open("./configs.json", 'r', encoding='utf-8') as json_file:
    dbconf = json.load(json_file)['db_config']


def exec_sql(sql, values, is_query=False):
    try:
        flag = False
        error = {}
        conn = pymysql.connect(host=dbconf['db_host'], port=dbconf['db_port'], user=dbconf['db_username'],
                               passwd=dbconf['db_password'], db=dbconf['db_database'], charset=dbconf['db_charset'])
        with conn.cursor(pymysql.cursors.DictCursor) as cursor:
            num = cursor.execute(sql, values)
        if is_query:
            result = cursor.fetchall()
        else:
            conn.commit()
        print('Sql: ', sql, ' Values: ', values)
    except Exception as err:
        flag = True
        error = err
        print('Error: ', err)
    finally:
        conn.close()
        if flag:
            return False, error, num if 'num' in dir() else 0
    return True, result if 'result' in dir() else '', num


def delete(tablename, params={}):
    sql = "delete from %s " % tablename
    sql += " where _id = %(_id)s "
    rs = exec_sql(sql, params)
    if rs[0]:
        return {"code": 200, "info": "delete success.", "total": rs[2]}
    else:
        return {"code": rs[1].args[0], "error": rs[1].args[1], "total": rs[2]}


def update(tablename, params={}):
    sql = "update %s set " % tablename
    ks = params.keys()
    for al in ks:
        sql += "`" + al + "` = %(" + al + ")s,"
    sql = sql[:-1]
    sql += " where _id = %(_id)s "
    rs = exec_sql(sql, params)
    if rs[0]:
        return {"code": 200, "info": "update success.", "total": rs[2]}
    else:
        return {"code": rs[1].args[0], "error": rs[1].args[1], "total": rs[2]}


def insert(tablename, params={}):
    sql = "insert into %s set " % tablename
    ks = params.keys()
    for al in ks:
        sql += "`" + al + "` = %(" + al + ")s,"
    sql = sql[:-1]
    rs = exec_sql(sql, params)
    if rs[0]:
        return {"code": 200, "info": "create success.", "total": rs[2]}
    else:
        return {"code": rs[1].args[0], "error": rs[1].args[1], "total": rs[2]}


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

    rs = exec_sql(sql+where, pvs, True)
    print('Result: ', rs)
    if rs[0]:
        return {"code": 200, "rows": rs[1], "total": rs[2]}
    else:
        return {"code": rs[1].args[0], "error": rs[1].args[1], "total": rs[2]}


# select('member', {'username': 'admin', "status": 1})
