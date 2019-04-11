# -*- coding: utf-8 -*-

"""
存储管理

存储使用七牛云存储的对象存储
@link https://developer.qiniu.com/kodo/sdk/1242/python
"""

import os
import sys

# 模块路径添加查找自定义包
sys.path.append('{dir}/app/packages'.format(dir=os.getcwd()))

from app.packages import qiniu
from config import ACCESS_KEY, SECRET_KEY, BUCKET_NAME


class Storage(object):
    __auth = None

    def __init__(self):
        self.__auth = qiniu.Auth(ACCESS_KEY, SECRET_KEY)

    def upload(self, local_path, remote_path):
        """
        本地文件上传
        """
        try:
            token = self.__auth.upload_token(BUCKET_NAME, remote_path, 3600)
            result, response = qiniu.put_file(token, remote_path, local_path)
            if result is not None and result['key'] == remote_path and result['hash'] == qiniu.etag(local_path):
                return result
            else:
                raise StorageException('message:{message} code:{code}'.format(message=response.error, code=response.status_code))
        except Exception as e:
            raise StorageException(e.message)

    def info(self, remote_path):
        """
        资源信息
        """
        try:
            bucket = qiniu.BucketManager(self.__auth)
            result, response = bucket.stat(BUCKET_NAME, remote_path)
            return result
        except Exception as e:
            raise StorageException(e.message)

    def is_exist(self, remote_path):
        """
        检查资源是否存在
        """
        try:
            result = self.info(remote_path)
            return result is not None
        except Exception as e:
            raise StorageException(e.message)


class StorageException(Exception):
    def __init__(self, message):
        super(StorageException, self).__init__(message)
