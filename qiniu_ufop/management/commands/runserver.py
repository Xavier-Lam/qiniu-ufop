# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop

from qiniu_ufop.utils import cpu_count, get_worker_instance
from qiniu_ufop.web import create_app
from ..base import BaseCommand


class Command(BaseCommand):
    def execute(self, args, unknown):
        app = get_worker_instance(args.app)
        debug = args.debug

        port = 9100

        application = create_app(
            app=app, debug=debug, autoreload=args.autoreload)
        if debug:
            application.listen(port)
        else:
            server = HTTPServer(application)
            server.bind(port)
            server.start(cpu_count())

        IOLoop().instance().start()

    def add_arguments(self):
        self.parser.add_argument("-A", "--app")
        self.parser.add_argument("--debug", action="store_true")
        self.parser.add_argument("--autoreload", action="store_true")
