# -*- coding: utf-8 -*-
from __future__ import unicode_literals

try:
    from io import BytesIO
except ImportError:
    from cStringIO import StringIO as BytesIO
import sys

from qiniu_ufop.web.dispatcher import Dispatcher
from qiniu_ufop.web.result import ResultHandler

from qiniu_ufop.utils import get_worker_instance
from ..base import BaseCommand


class Command(BaseCommand):
    def execute(self, args, unknown):
        app = get_worker_instance(args.app)
        dispatcher = Dispatcher(app, preserve_name=True)
        result_handler = ResultHandler()
        with open(args.filename, "rb") as f:
            buffer = BytesIO(f.read())
            task = dispatcher.dispatch(buffer, args.cmd, args.content_type)
            result = task()
            response = result_handler.make_response(result)
            sys.stdout.buffer.write(response.body)

    def add_arguments(self):
        self.parser.add_argument("cmd", default="", nargs="?")
        self.parser.add_argument("filename")
        self.parser.add_argument("-A", "--app")
        self.parser.add_argument("--content-type")
