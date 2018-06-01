# -*- coding: utf-8 -*-
# flake8: noqa
# @absurdity @real
__author__ = 'nosoyyo'
__version__ = {'0.1': '2018.01',
               '0.2': '2018.02',
               '0.3': '2018.05.23',
               '0.4': '2018.05.31',
               }

# 0.1 basically setup
# 0.2 base class changed into singleton mode; added user/pwd auth;
# 0.3 removed singleton mode, added basic CRUD method wrappers
# 0.4 add `ls` behaviour customization

import os
import logging
import pymongo
from bson.objectid import ObjectId
from pymongo.collection import Collection

from .exception import InvalidCollectionError


settings = {}
settings['MONGODB_SERVER'] = os.environ.get('RABONA_MONGODB_SERVER')
settings['MONGODB_PORT'] = int(os.environ.get('RABONA_MONGODB_PORT'))
settings['MONGODB_USERNAME'] = os.environ.get('RABONA_MONGODB_USERNAME')
settings['MONGODB_PASSWORD'] = os.environ.get('RABONA_MONGODB_PASSWORD')
settings['MONGODB_RABONA_DB'] = 'rabona'
settings['MONGODB_INIT_COL'] = 'testcol'

# init
if 'log' not in os.listdir():
    os.mkdir('log')

logging.basicConfig(
    filename='var/log/mongodb.log',
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

    def dealWithCol(self, _col=None) -> Collection:
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
            logging.error('dealWithCol raises {}'.format(e))

    def insert(self, doc: dict, col: str=None) -> ObjectId:
        col = self.dealWithCol(col)
        try:
            oid = col.insert_one(doc).inserted_id
            if isinstance(oid, ObjectId):
                logging.debug('doc {} inserted into {}'.format(doc, col.name))
                return oid
        except Exception as e:
            logging.error('pipeline.insert() raises {}'.format(e))

    def ls(self, arg=None, col=None, **kwargs):
        col = self.dealWithCol(col)

        if arg is None:
            return self.db.collection_names()
        elif isinstance(arg, str):
            col = self.dealWithCol(arg)
            return [item for item in col.find()]
        elif isinstance(arg, int) and col is None:
            col = self.ls()[arg]
            return self.ls(col)
        elif isinstance(arg, dict):
            logging.debug('looking for {} in "{}"'.format(arg, col.name))
            return [item for item in col.find(arg)]
        elif isinstance(arg, ObjectId):
            return col.find_one({'_id': arg})
        elif col.name in self.custom_ls_behaviour_col:
            return self.custom_ls(arg=arg, col=col, **kwargs)
        elif kwargs:
            # TODO
            return col.find_one(kwargs)

    def update(self, oid: ObjectId, doc: dict, col: str=None) -> bool:
        col = self.dealWithCol(col)

        try:
            result = col.update_one({'_id': oid}, {"$set": doc},)
            if result.modified_count:
                logging.debug('updated {} in {}, result[{}]'.format(
                    doc, col.name, result))
                boolean = True
            else:
                if result.matched_count:
                    logging.debug('{} not updated in {}, input same to output.'.format(
                        doc, col.name, result))
                    boolean = False
                else:
                    logging.debug('{} not updated in {}, nothing matches input.'.format(
                        doc, col.name, result))
                    boolean = False

            return boolean
        except Exception as e:
            logging.error('m.update raises {}'.format(e))
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
                logging.error(
                    'm.rm raises {} during deleting by ObjectId'.format(e))
                return False
        elif isinstance(arg, dict):
            try:
                if '_id' in arg.keys() and isinstance(arg['_id'], ObjectId):
                    return self.rm(arg['_id'], col)
                else:
                    return False
            except Exception as e:
                logging.error('m.rm raises {} during deleting doc'.format(e))
                return False
        else:
            return False
