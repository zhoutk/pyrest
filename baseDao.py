import dbhelper


class BaseDao(object):

    def __init__(self, table):
        self.table = table

    def retrieve(self, params, fields=[], session={}):
        return dbhelper.select(self.table, params)

    def create(self, params, fields=[], session={}):
        return dbhelper.insert(self.table, params)

    def update(self, params, fields=[], session={}):
        return dbhelper.update(self.table, params)

    def delete(self, params, fields=[], session={}):
        return dbhelper.delete(self.table, params)
