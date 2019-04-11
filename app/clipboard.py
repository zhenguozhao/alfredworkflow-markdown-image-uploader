# -*- coding: utf-8 -*-

"""
剪切板管理
"""

import os
from collections import defaultdict
from AppKit import NSPasteboard, NSFilenamesPboardType, NSPasteboardTypePNG


class Clipboard(object):
    @property
    def support_type(self):
        return ('tiff', 'png', 'jpeg', 'jpg', 'gif')

    @property
    def image(self):
        """
        获取图片信息
        """
        image = defaultdict(lambda: None)
        clipboard = NSPasteboard.generalPasteboard()
        clipboard_content_type = clipboard.types()
        if NSFilenamesPboardType in clipboard_content_type or NSPasteboardTypePNG in clipboard_content_type:
            # 文件清理标识
            clean = True
            file_path = None
            if NSFilenamesPboardType in clipboard_content_type:
                """
                剪切板内容是"文件"
                
                这里只考虑文件单选的情况，多文件需要额外处理
                """
                file_path = clipboard.propertyListForType_(NSFilenamesPboardType)[0]
                clean = False
            elif NSPasteboardTypePNG in clipboard_content_type:
                """
                剪切板内容是"截图"
                """
                file_path = '/tmp/{file}'.format(file=NSPasteboardTypePNG)
                # 写入临时磁盘文件
                result = clipboard.dataForType_(NSPasteboardTypePNG).writeToFile_atomically_(file_path, False)
                if result is not True:
                    raise FileWriteException(file_path)
                clean = True
            # 文件类型依赖文件扩展名
            file_type = os.path.splitext(file_path)[1][1:].lower()
            if file_type not in self.support_type:
                raise FileTypeUnsupportedException(file_type)

            image['file'] = file_path
            image['type'] = file_type
            image['clean'] = clean

        if image['file'] is None:
            raise ImageNotFoundException()

        return image


class FileWriteException(Exception):
    def __init__(self, file_path):
        super(FileWriteException, self).__init__('文件 {file_path} 写入磁盘异常！'.format(file_path=file_path))


class FileTypeUnsupportedException(Exception):
    def __init__(self, file_type):
        super(FileTypeUnsupportedException, self).__init__('不支持的文件类型：{file_type}'.format(file_type=file_type))


class ImageNotFoundException(Exception):
    def __init__(self):
        super(ImageNotFoundException, self).__init__('请先复制图片或截图再进行操作！')
