# ================
# Qiniu quickstart
# ================

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

from qiniu import Auth, BucketManager, put_file, etag, urlsafe_base64_encode
from .config import QiniuConf


class QiniuPipeline():

    def __init__(self):
        self.settings = QiniuConf.__dict__
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
        ls = self.bucket.list(self.bucket_name)[0]['items']
        return ls

    def count(self):
        c = len(self.bucket.list(self.bucket_name)[0]['items'])
        return c
