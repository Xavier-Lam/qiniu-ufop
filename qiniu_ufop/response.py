# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from tornado.httputil import HTTPHeaders, responses


class Response(object):
    def __init__(self, code=200, headers=None, body=None, buffer=None,
                 reason=None):
        self.code = code
        self.reason = reason or responses.get(code, "Unknown")
        self.buffer = buffer
        self.headers = headers or HTTPHeaders()
        self._body = body

    @property
    def body(self):
        if self._body is None:
            self._body = "" if self.buffer is None else self.buffer.getvalue()
        return self._body
