# -*- coding: utf-8 -*-

import sys
import os
import logging
import hashlib
from app.clipboard import Clipboard, FileWriteException, FileTypeUnsupportedException, ImageNotFoundException
from app.storage import Storage, StorageException
from app.config import ACCESS_KEY, SECRET_KEY, BUCKET_NAME, RESOURCE_PREFIX, IMAGE_TEMPLATE, MARKDOWN_IMAGE_TEMPLATE
from app.setting import LOGGING_SETTING
from app.packages.workflow.notify import notify

# 指定编码解码方式
reload(sys)
sys.setdefaultencoding('utf-8')

logging.basicConfig(**LOGGING_SETTING)
exception = (FileWriteException, FileTypeUnsupportedException, ImageNotFoundException, StorageException)


def file_hash(file_path):
    hash = hashlib.md5()
    with open(file_path, "rb") as file:
        while True:
            content = file.read(65535)
            if 0 == len(content):
                break
            hash.update(content)
    return hash.hexdigest()


def open_editor(file_path):
    os.system('open -e "{file}"'.format(file=file_path))


def main():
    # 检查存储配置信息
    if not all((ACCESS_KEY, SECRET_KEY, BUCKET_NAME, RESOURCE_PREFIX)):
        notify('⚠️ 警告', '请先设置好相关配置信息！')
        open_editor('app/config.py')
        return

    try:
        """
        文件上传
        """
        image = Clipboard().image
        logging.debug('image info: {image}'.format(image=image))
        local_path = image['file']
        remote_path = '{name}.{postfix}'.format(name=file_hash(local_path), postfix=image['type'])
        storage = Storage()
        if not storage.is_exist(remote_path):
            storage.upload(local_path, remote_path)
        if image['clean'] is True:
            # 清理磁盘临时文件
            os.remove(local_path)
        notify('📢 通知', '文件上传成功！')

        """
        文件展示
        """
        url = '{prefix}/{path}{template}'.format(prefix=RESOURCE_PREFIX.strip('/'), path=remote_path, template=IMAGE_TEMPLATE)
        if not url.startswith("http://"):
            url = "http://" + url
        # 处理markdown图片模板占位符
        markdown_data = {}
        for item in ('title', 'url'):
            if '{%(mark)s}' % {'mark': item} in MARKDOWN_IMAGE_TEMPLATE:
                if item == 'title':
                    markdown_data['title'] = remote_path
                elif item == 'url':
                    markdown_data['url'] = url
        logging.debug('markdown data: {markdown_data}'.format(markdown_data=markdown_data))
        print MARKDOWN_IMAGE_TEMPLATE.format(**markdown_data)
    except exception as e:
        notify('❌ 错误', str(e))


if __name__ == '__main__':
    main()
