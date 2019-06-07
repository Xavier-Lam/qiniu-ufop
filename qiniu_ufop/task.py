# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os

from celery import Celery, Task as BaseTask


os.environ.setdefault("CELERY_BROKER_URL", "redis://localhost:6379/0")
os.environ.setdefault("CELERY_RESULT_BACKEND", "redis://localhost:6379/0")


class QiniuUFOP(Celery):
    task_cls = 'qiniu_ufop:Task'
    routes = []

    def __init__(self, **kwargs):
        changes = kwargs.get("changes") or {}
        changes.update(
            accept_content=["pickle"],
            task_serializer="pickle",
            result_serializer="pickle",
            event_serializer="pickle"
        )
        kwargs["changes"] = changes
        super(QiniuUFOP, self).__init__(**kwargs)

    def task(self, *args, **opts):
        opts["lazy"] = False
        return super(QiniuUFOP, self).task(*args, **opts)

    def _task_from_fun(self, fun, **options):
        """注册路由"""
        route = options.pop("route", None)
        base = options.get("base")
        if base:
            if not isinstance(base, Task):
                raise ValueError
            route = base.route

        task = super(QiniuUFOP, self)._task_from_fun(fun, **options)
        route and self.routes.append((route, task))
        return task


class Task(BaseTask):
    route = None

    def health(self):
        pass
