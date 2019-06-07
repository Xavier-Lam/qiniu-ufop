# -*- coding: utf-8 -*-
from __future__ import unicode_literals

try:
    from io import BytesIO
except ImportError:
    from cStringIO import StringIO as BytesIO

from kombu.utils.imports import symbol_by_name
from kombu.utils.objects import cached_property
from tornado.concurrent import Future
from tornado.gen import coroutine
from tornado.httpclient import AsyncHTTPClient
from tornado.ioloop import IOLoop
from tornado.web import RequestHandler

__all__ = ("HandlerController", "HealthController")


class BaseController(RequestHandler):
    @property
    def dispatcher(self):
        """:rtype: qiniu_ufop.web.dispatcher.AbstractDispatcher"""
        return self.application.dispatcher


class HandlerController(BaseController):
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
            buffer = BytesIO(self.request.body)
            content_type = self.request.headers.get("Content-Type")

        task = self.dispatcher.dispatch(
            buffer, cmd, content_type, self.request)
        job = self.apply(task)
        future = self.make_future(job)
        yield future
        result = future.result()
        response = self.result_handler.make_response(result)

        self.send(response)
        self.finish()

    def apply(self, task):
        return task.apply_async()

    def make_future(self, job):
        def check_status(job, future):
            if job.ready():
                future.set_result(job.result)
            else:
                IOLoop.current().call_later(0.1, check_status, job, future)

        future = Future()
        check_status(job, future)
        return future

    def send(self, response):
        self.set_status(response.code, response.reason)
        for header, value in response.headers.items():
            self.set_header(header, value)
        self.write(response.body)

    @cached_property
    def result_handler(self):
        """:rtype: qiniu_ufop.web.result.ResultHandler"""
        cls = self.application.settings.get(
            "ufop_dispatcher", "qiniu_ufop.web.result.ResultHandler")
        return symbol_by_name(cls)()


class HealthController(BaseController):
    """健康检查控制器"""
    def get(self):
        """健康检查控制器应响应200 OK的空串"""
        for handler in self.dispatcher.listall():
            if hasattr(handler, "health"):
                handler.health()
        self.write("")
        self.finish()
