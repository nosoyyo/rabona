# -*- coding: utf-8 -*-
# flake8: noqa
# @absurdity @real
__author__ = 'nosoyyo'

# 1801?? 0.1 basically setup
# 1802?? 0.2 base class changed into singleton mode; added user/pwd auth;
# 180523 0.3 removed singleton mode, added basic CRUD method wrappers

import os
import logging
import pymongo
from bson.objectid import ObjectId
from pymongo.collection import Collection

from .exceptions import InvalidCollectionError


settings = {}
settings['MONGODB_SERVER'] = os.environ.get('RABONA_MONGODB_SERVER')
settings['MONGODB_PORT'] = int(os.environ.get('RABONA_MONGODB_PORT'))
settings['MONGODB_USERNAME'] = os.environ.get('RABONA_MONGODB_USERNAME')
settings['MONGODB_PASSWORD'] = os.environ.get('RABONA_MONGODB_PASSWORD')
settings['MONGODB_RABONA_DB'] = 'rabona'
settings['MONGODB_INIT_COL'] = 'testcol'

# init
logging.basicConfig(
    filename='log/mongodb.log',
    level=logging.INFO,
    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s')


# ==================
# MongoDB quickstart
# ==================
class MongoDBPipeline():
    client = pymongo.MongoClient(
        settings['MONGODB_SERVER'],
        settings['MONGODB_PORT'],
    )
    db = client.get_database(settings['MONGODB_RABONA_DB'])
    auth = db.authenticate(
        settings['MONGODB_USERNAME'],
        settings['MONGODB_PASSWORD']
    )
    col = db.get_collection(settings['MONGODB_INIT_COL'])

    def setDB(self, dbname):
        self.db = self.client.get_database(dbname)
        return self

    def setCol(self, colname, dbname=None):
        if dbname:
            self.db = self.client.get_database(dbname)
        return self.db.get_collection(colname)

    def dealWithCol(self, _col=None):
        try:
            if not _col:
                col = self.col
            elif isinstance(_col, Collection):
                col = _col
            elif isinstance(_col, str):
                col = self.setCol(_col)
            else:
                raise InvalidCollectionError(_col)
            return col
        except Exception as e:
            print(e)

    def insert(self, doc, col=None):
        col = self.dealWithCol(col)
        try:
            oid = col.insert_one(doc).inserted_id
            if isinstance(oid, ObjectId):
                logging.info('doc {} inserted into {}'.format(doc, col.name))
                return oid
        except Exception as e:
            print(e)
            return False

    def ls(self, arg=None, col=None):
        col = self.dealWithCol(col)

        if arg is None:
            return self.db.collection_names()
        elif isinstance(arg, str):
            col = self.dealWithCol(arg)
            print('listing collection "{}"'.format(col.name))
            return [item for item in col.find()]
        elif isinstance(arg, int) and col is None:
            col = self.ls()[arg]
            return self.ls(col)
        elif isinstance(arg, dict):
            print('looking for {} in "{}"'.format(arg, col.name))
            return [item for item in col.find(arg)]
        elif isinstance(arg, ObjectId):
            return col.find_one({'_id': arg})

    def update(self, oid, doc, col=None):
        col = self.dealWithCol(col)

        try:
            result = bool(col.update_one(
                {'_id': oid},
                {"$set": doc},
                upsert=False
            ).raw_result['nModified']) or False
            logging.info('updating {} in {}, result[{}]'.format(
                doc, col.name, result))
            return result
        except Exception as e:
            print(e)
            return False

    def rm(self, arg, col=None):
        '''
        Only supports deleting by oid for now.

        :param oid: `bson.objectid.ObjectId`
        '''
        col = self.dealWithCol(col)

        if isinstance(arg, ObjectId):
            try:
                result = bool(col.delete_one(
                    {'_id': arg}).raw_result['n']) or False
                logging.info('deleting {} in {}, result[{}]'.format(
                    arg, col.name, result))
                return result
            except Exception as e:
                print(e)
                return False
        elif isinstance(arg, dict):
            try:
                if '_id' in arg.keys() and isinstance(arg['_id'], ObjectId):
                    return self.rm(arg['_id'], col)
                else:
                    return False
            except Exception as e:
                print(e)
                return False
        else:
            return False
