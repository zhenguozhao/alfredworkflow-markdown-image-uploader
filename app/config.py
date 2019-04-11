# -*- coding: utf-8 -*-

"""
存储配置信息

存储使用七牛云存储的对象存储
@link https://developer.qiniu.com/kodo/
"""

# 帐号密钥对
ACCESS_KEY = ""
SECRET_KEY = ""

# 存储空间名称
BUCKET_NAME = ""

# 资源访问前缀
RESOURCE_PREFIX = ""
"""
图片样式，包括样式分隔符，可不设置为空
@link https://developer.qiniu.com/kodo/kb/1327/what-is-the-style-and-the-style-separators
"""
IMAGE_TEMPLATE = ""

"""
markdown图片模板

支持的占位符：
{title} 图片名称
{url} 图片地址
"""
MARKDOWN_IMAGE_TEMPLATE = "![{title}]({url})"
