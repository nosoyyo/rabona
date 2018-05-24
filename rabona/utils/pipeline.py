# -*- coding: utf-8 -*-
# flake8: noqa
# @absurdity @real
__author__ = 'nosoyyo'


# usage
#
# from web to qiniu:
# q = QiniuPipeline()
# pic_url = 'http://some.pic.url'
# ret = q.upload(pic_url)
#
# from qiniu to distribution:
# q = QiniuPipeline()
# downloadable_file_url = q.getFile(key)

# 1801?? 0.1 basically setup
# 1802?? 0.2 base class changed into singleton mode; added user/pwd auth;
# 180523 0.3 removed singleton mode, added basic CRUD method wrappers

import logging
import pymongo
from bson.objectid import ObjectId
from pymongo.collection import Collection

from .config import MongoConf, QiniuConf
from .exceptions import InvalidCollectionError


# init
logging.basicConfig(
    filename='log/mongodb.log',
    level=logging.INFO,
    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s')


# ==================
# MongoDB quickstart
# ==================
class MongoDBPipeline():
    settings = MongoConf.__dict__
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
            result = col.insert(doc)
            if isinstance(result, ObjectId):
                logging.info('doc {} inserted into {}'.format(doc, col.name))
                return result
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
        elif isinstance(arg, int):
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
            doc_origin = self.ls(oid, col)
            ks, vs = [k for k in doc.keys()], [
                v for v in doc.values()]
            for i in range(len(doc)):
                doc_origin[ks[i]] = vs[i]

            result = bool(col.update(
                {'_id': oid}, doc_origin, upsert=False)['n']) or False
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


# ================
# Qiniu quickstart
# ================

class QiniuPipeline():

    # import
    from qiniu import Auth, BucketManager, put_file, etag, urlsafe_base64_encode
    import qiniu.config

    def __init__(self):
        self.settings = QiniuConf.__annotations__
        self.m = MongoDBPipeline()
        self.m_auth = self.m.auth
        self.access_key = self.settings['QINIU_ACCESS_KEY']
        self.secret_key = self.settings['QINIU_SECRET_KEY']

        # 构建鉴权对象
        self.auth = self.Auth(self.access_key, self.secret_key)

        # bucket
        self.bucket = BucketManager(self.auth)

        # 要上传的空间
        self.bucket_name = self.settings['QINIU_BUCKET_NAME']

        # 上传到七牛后保存的文件名前缀
        self.prefix = 'rabona'

    def upload(self, pic_url):
        bucket_name = self.bucket_name
        key = pic_url.split('/')[-1]
        token = self.auth.upload_token(bucket_name, key, 0)
        ret = self.bucket.fetch(pic_url, bucket_name, key)
        return ret

    def getFile(self, key):
        url = self.auth.private_download_url(self.settings['QINIU_URL'] + key)
        return url

    def ls(self):
        l = self.bucket.list(self.bucket_name)[0]['items']
        return l

    def count(self):
        c = len(self.bucket.list(self.bucket_name)[0]['items'])
        return c
