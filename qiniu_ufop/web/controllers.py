# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import re

from six.moves import cStringIO as StringIO
from tornado.gen import coroutine, Task
from tornado.httpclient import AsyncHTTPClient
from tornado.web import RequestHandler

__all__ = ("HandlerController", "HealthController")


class HandlerController(RequestHandler):
    """处理自定义业务控制器"""

    @coroutine
    def post(self):
        cmd = self.get_argument("cmd")
        url = self.get_argument("url", None)
        if url:
            client = AsyncHTTPClient()
            resp = yield client.fetch(url)
            buffer = resp.buffer
            content_type = resp.headers.get("Content-Type")
        else:
            # 从POST body直接读取
            buffer = StringIO(self.request.body)
            content_type = self.request.headers.get("Content-Type")

        response = yield self.dispatch(buffer, cmd, content_type)
        result = self.handle_result(response.result)
        # self.set_header()
        # self.write()
        # self.finish()

    def dispatch(self, buffer, cmd, content_type):
        """根据cmd派发任务"""
        task, args = self.parse_cmd(cmd)
        return Task(task, args=(buffer, args, content_type))

    def parse_cmd(self, cmd):
        """将cmd拆解为传给task的arguments"""
        for route, task in self.application.celery.routers:
            match = re.search(cmd, route)
            if match:
                return task, match.groupdict()
        else:
            raise ValueError # not found

    def handle_result(self, result):
        """处理任务结果"""
        return result


class HealthController(RequestHandler):
    """健康检查控制器"""

    def get(self):
        """健康检查控制器应响应200 OK的空串"""
        self.write("")
        self.finish()
