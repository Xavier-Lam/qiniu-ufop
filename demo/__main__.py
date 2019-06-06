# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from qiniu_ufop import QiniuUFOP


ufop = QiniuUFOP()

@ufop.task(route=r"/debug")
def debug(buffer, args, content_type):
    return buffer
