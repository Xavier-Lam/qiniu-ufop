# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import re


class AbstractDispatcher(object):
    def __init__(self, application, preserve_name=False):
        self.application = application
        self.preserve_name = preserve_name

    def dispatch(self, buffer, cmd, content_type, request):
        raise NotImplementedError()

    def listall(self):
        raise NotImplementedError()


class Dispatcher(AbstractDispatcher):
    def dispatch(self, buffer, cmd, content_type, request=None):
        """根据cmd派发任务"""
        task, args = self.parse_cmd(cmd)
        return task.s(buffer, args, content_type)

    def parse_cmd(self, cmd):
        """将cmd拆解为传给task的arguments"""
        if not self.preserve_name:
            cmd = re.sub(r"^[^/]+", "", cmd)  # 第一个是ufop名 无用
        for route, task in self.application.routes:
            match = re.search(route, cmd)
            if match:
                return task, match.groupdict()
        else:
            raise ValueError  # not found

    def listall(self):
        return dict(self.application.routes).values()
