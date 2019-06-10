# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop

from qiniu_ufop.utils import cpu_count, get_worker_instance
from qiniu_ufop.web import create_app
from ..base import BaseCommand


class Command(BaseCommand):
    """运行web服务"""

    def execute(self, args, unknown):
        app = get_worker_instance(args.app)
        debug = args.debug
        webapp = args.webapp

        port = args.port

        application = create_app(
            webapp, app=app, debug=debug, autoreload=args.autoreload)
        if debug:
            application.listen(port)
        else:
            server = HTTPServer(application)
            server.bind(port)
            server.start(args.num_processes or cpu_count())

        IOLoop().current().start()

    def add_arguments(self):
        self.parser.add_argument("-A", "--app")
        self.parser.add_argument(
            "--webapp", default="qiniu_ufop.web.Application",
            help="web默认cls")
        self.parser.add_argument(
            "--debug", action="store_true", help="开启调试模式")
        self.parser.add_argument(
            "--autoreload", action="store_true", help="开启自动加载")
        self.parser.add_argument(
            "--num-processes", type=int, help="进程数")
        self.parser.add_argument(
            "-p", "--port", type=int, default=9100, help="运行端口")
