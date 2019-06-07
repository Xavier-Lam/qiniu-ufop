# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from qiniu_ufop import QiniuUFOP


ufop = QiniuUFOP()


@ufop.task(route=r"^/hello(?:/(?P<name>\w+))?$")
def hello(buffer, args, content_type):
    """参数处理"""
    return "hello " + args.get("name", "world")


@ufop.task(route=r"^/json")
def json(buffer, args, content_type):
    """返回json"""
    return dict(
        msg="this is a json response",
        content_type=content_type
    )

@ufop.task(route=r".*")
def handler(buffer, args, content_type):
    """原样输出"""
    return buffer.read()
