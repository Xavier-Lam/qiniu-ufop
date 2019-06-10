# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from kombu.utils.imports import symbol_by_name
from kombu.utils.objects import cached_property
import six
from tornado.web import Application as BaseApplication

from . import controllers as c


class Application(BaseApplication):
    @cached_property
    def celery(self):
        """:rtype: qiniu_ufop.task.QiniuUFOP"""
        obj = self.settings["app"]
        if isinstance(obj, six.text_type):
            return symbol_by_name(obj)
        return obj

    @cached_property
    def dispatcher(self):
        """:rtype: qiniu_ufop.web.disapcher.Dispatcher"""
        cls = self.settings.get(
            "ufop_dispatcher", "qiniu_ufop.web.dispatcher.Dispatcher")
        return symbol_by_name(cls)(self.celery)


def create_app(cls_name, **settings):
    cls = symbol_by_name(cls_name)
    return cls(
        handlers=(
            (r"/health/?", c.HealthController),
            (r"/handler/?", c.HandlerController)
        ),
        **settings
    )
