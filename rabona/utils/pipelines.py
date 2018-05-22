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

# 0.1 basically setup
# 0.2 base class changed into singleton mode; added user/pwd auth;

import pymongo
from config import MongoDBConfig, QiniuConfig

# init
settings = {
    #'MONGODB_SERVER' : 'localhost',
    'MONGODB_SERVER': MongoDBConfig.MONGODB_SERVER
    'MONGODB_PORT': MongoDBConfig.MONGODB_PORT

    'MONGODB_USERNAME': MongoDBConfig.MONGODB_USERNAME
    'MONGODB_PASSWORD': MongoDBConfig.MONGODB_PASSWORD

    'MONGODB_DB': MongoDBConfig.MONGODB_DB
    'MONGODB_COL': MongoDBConfig.MONGODB_COL

    # Qiniu
    'BUCKET_NAME': QiniuConfig.BUCKET_NAME
    'QINIU_USERNAME': QiniuConfig.QINIU_USERNAME
    'QINIU_PROFILE': QiniuConfig.QINIU_PROFILE
    'QINIU_PRIVATE': QiniuConfig.QINIU_PRIVATE

}

# ==================
# MongoDB quickstart
# ==================


class Singleton(object):
    _instance = None

    def __new__(cls, dbname, username, password, *args, **kw):
        if not cls._instance:
            cls._instance = super(Singleton, cls).__new__(cls, *args, **kw)
        return cls._instance


class MongoDBPipeline(Singleton):

    def __init__(self, dbname, username, password, settings=settings, ):

        self.client = pymongo.MongoClient(
            settings['MONGODB_SERVER'],
            settings['MONGODB_PORT'],
            username=username,
            password=password,
        )
        self.db = self.client.get_database(dbname)
        self.auth = self.db.authenticate(username, password)
        self.col = self.db.get_collection(settings['MONGODB_COL'])

    def setDB(self, dbname):
        self.db = self.client.get_database(dbname)
        return self

    def setCol(self, dbname, colname):
        self.db = self.client.get_database(dbname)
        self.col = self.db.get_collection(colname)
        return self

    def ls(self):
        return self.db.list_collection_names()


# ================
# Qiniu quickstart
# ================

class QiniuPipeline():

    # import
    from qiniu import Auth, BucketManager, put_file, etag, urlsafe_base64_encode
    import qiniu.config

    def __init__(self, dbname, username, password):
        self.m = MongoDBPipeline(dbname, username, password)
        self.m_auth = self.m.auth
        self.keys = self.m.setCol(
            settings['QINIU_USERNAME'], settings['QINIU_PROFILE']).col.find()[0]['keys']
        self.access_key = self.keys['access_key']
        self.secret_key = self.keys['secret_key']

        # 构建鉴权对象
        self.auth = self.Auth(self.access_key, self.secret_key)

        # bucket
        self.bucket = BucketManager(self.auth)

    # 要上传的空间
    bucket_name = settings['BUCKET_NAME']

    # 上传到七牛后保存的文件名前缀
    prefix = 'rabona'

    def upload(self, pic_url):
        bucket_name = self.bucket_name
        key = pic_url.split('/')[-1]
        token = self.auth.upload_token(bucket_name, key, 0)
        ret = self.bucket.fetch(pic_url, bucket_name, key)
        return ret

    def getFile(self, key):
        url = self.auth.private_download_url(settings['QINIU_PRIVATE'] + key)
        return url

    def ls(self):
        l = self.bucket.list(self.bucket_name)[0]['items']
        return l

    def count(self):
        c = len(self.bucket.list(self.bucket_name)[0]['items'])
        return c
