# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os

from kombu.utils.imports import symbol_by_name
from kombu.utils.objects import cached_property
import tcelery
from tornado.web import Application as BaseApplication

from . import controllers as c


class Application(BaseApplication):
    @cached_property
    def celery(self):
        """:rtype: qiniu_ufop.task.UFOPCelery"""
        obj_str = self.settings["ufop_celery"]
        return symbol_by_name(obj_str)


def create_app(**settings):
    tcelery.setup_nonblocking_producer()
    return Application(
        handlers=(
            (r"/", c.HealthController),
            (r"/handler", c.HandlerController)
        ),
        **settings
    )
