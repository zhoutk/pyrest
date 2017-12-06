import dbhelper


class Basedao(object):

    def __init__(self, table):
        self.table = table

    def retrieve(self, params, fields=[], session={}):
        return dbhelper.select(self.table, params)
