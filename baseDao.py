import dbhelper


class BaseDao(object):

    def __init__(self, table):
        self.table = table

    def retrieve(self, params={}, fields=[], session={}):
        return dbhelper.select(self.table, params)

    def create(self, params={}, fields=[], session={}):
        if '_id' in params and len(params) < 2 or '_id' not in params and len(params) < 1:
            return {"code": 301, "err": "The params is error."}
        return dbhelper.insert(self.table, params)

    def update(self, params={}, fields=[], session={}):
        if '_id' in params and len(params) < 2 or '_id' not in params and len(params) < 1:
            return {"code": 301, "err": "The params is error."}
        return dbhelper.update(self.table, params)

    def delete(self, params={}, fields=[], session={}):
        if '_id' not in params:
            return {"code": 301, "err": "The params is error."}
        return dbhelper.delete(self.table, params)
