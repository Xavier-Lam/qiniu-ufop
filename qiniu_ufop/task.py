# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from celery import Celery, Task as BaseTask


class QiniuUFOP(Celery):
    task_cls = 'qiniu_ufop:Task'
    routes = []

    def _task_from_fun(self, fun, **options):
        """注册路由"""
        route = options.pop("route", None)
        base = options.get("base")
        if base:
            if not isinstance(base, Task):
                raise ValueError
            route = base.route

        if not route:
            raise ValueError

        task = super(QiniuUFOP, self)._task_from_fun(fun, **options)
        self.routes.append((route, task))
        return task


class Task(BaseTask):
    route = None
