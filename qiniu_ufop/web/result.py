# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json

import six

from ..response import Response


class ResultHandler(object):
    def make_response(self, result):
        """
        处理任务结果
        :rtype: qiniu_ufop.response.Response
        """
        buffer = None
        body = None
        content_type = None

        if isinstance(result, tuple):
            result, content_type = result
        if isinstance(result, (dict, list)):
            body = json.dumps(result).encode("utf-8")
            content_type = content_type or "application/json; charset=utf-8"
        elif isinstance(result, six.text_type):
            body = result.encode("utf-8")
            content_type = content_type or "text/plain; charset=utf-8"
        elif not isinstance(result, Response):
            body = result

        if not isinstance(result, Response):
            result = Response(body=body, buffer=buffer)

        if content_type:
            result.headers["Content-Type"] = content_type

        return result
