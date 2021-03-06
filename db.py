#!/usr/bin/env python
# encoding:utf-8
# db.py
# 2016/9/27  22:02
from pymongo import MongoClient, collection
from pymongo import collection
class DB(object):
    def __init__(self, url='127.0.0.1', port=27017, user=None, password=None, db='test'):
        if user is None or password is None:
            self.conn   =  MongoClient("mongodb://%s" % url, 27017)
        else:
            self.conn = MongoClient("mongodb://%s:%s@%s" % (user, password, url), 27017)
        self.db = self.conn[db]

    def get_db(self, table):
        return self.db[table]

    def insert_unexist(self, table, keys, data):
        filter_key = {}
        if not isinstance(keys, list):
            keys = [keys]

        for key in keys:
            filter_key[key] = data[key]

        found = self.find_one(table, filter_key)
        if found:
            return False
        else:
            return self.insert(table, keys, data)


    def insert(self, table, keys, data):
        """将一条记录存储到数据库中(若已存在则更新)
        :param table:   str, 待插入的表名(collection)
        :param filter:  str|array(str), 过滤用，防止插入重复记录
        :return:        dict, {'updatedExisting': True, u'nModified': 0, u'ok': 1, u'n': 1}
        """
        if isinstance(keys, basestring):
            keys = [keys]
        elif isinstance(keys, list):
            pass
        else:
            keys = []

        #{'id': data['id']}
        filter_key  = {}
        for key in keys:
            filter_key[key] = data[key]

        return self.db[table].update_one(filter_key, {'$set':data}, True).raw_result

    def find_one(self, table, query=None):
        return self.db[table].find_one(query)

    def find(self, table, query=None):
        return self.db[table].find(query)

    def remove(self, table, query=None, multi=True, **kwargs):
        return self.db[table].remove(query,multi,**kwargs)