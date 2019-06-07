# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import argparse
import os
import sys


def _cpu_count():
    from tornado.process import cpu_count
    return cpu_count()


def _get_app(args):
    from kombu.utils.imports import symbol_by_name

    app = args.app or os.getenv("QINIU_UFOP_CELERY")
    if not app:
        #  app默认取当前工作路径的app.ufop
        sys.path.append(os.getcwd())
        app = "app.ufop"
    celery = symbol_by_name(app)
    return celery


def createproject(args, unknown):
    from shutil import copyfile

    from qiniu_ufop import demo

    if args.dir and not os.path.exists(args.dir):
        os.makedirs(args.dir)
    copyfile(demo.__file__, os.path.join(args.dir, "app.py"))
    requirements = os.path.join(args.dir, "requirements.txt")
    if not os.path.exists(requirements):
        open(requirements, "a").close()
    envs = os.path.join(args.dir, ".env")
    if not os.path.exists(envs):
        with open(envs, "a") as f:
            f.writelines(("# export your environments here",))


def createdockerfile(args, unknown):
    import qiniu_ufop

    datadir = os.path.join(os.path.dirname(qiniu_ufop.__file__), "data")
    with open(os.path.join(datadir, "Dockerfile"), "r", encoding="utf-8") as f:
        dir = os.path.abspath(args.dir)
        sys.stdout.buffer.write(f.read().format(
            DIR=dir,
            DATADIR=datadir
        ).encode(args.encoding))


def proccess(args, unknown):
    try:
        from io import BytesIO
    except ImportError:
        from cStringIO import StringIO as BytesIO

    from qiniu_ufop.web import create_app
    from qiniu_ufop.web.dispatcher import Dispatcher
    from qiniu_ufop.web.result import ResultHandler

    app = _get_app(args)
    dispatcher = Dispatcher(app, preserve_name=True)
    result_handler = ResultHandler()
    with open(args.filename, "rb") as f:
        buffer = BytesIO(f.read())
        task = dispatcher.dispatch(buffer, args.cmd, args.content_type)
        result = task()
        response = result_handler.make_response(result)
        sys.stdout.buffer.write(response.body)


def runworker(args, unknown):
    app = _get_app(args)
    app.worker_main(["worker"] + unknown)


def runserver(args, unknown):
    from tornado.httpserver import HTTPServer
    from tornado.ioloop import IOLoop

    from qiniu_ufop.web import create_app

    app = _get_app(args)
    debug = args.debug

    port = 9100
    cpu_count = _cpu_count()

    application = create_app(
        app=app, debug=debug, autoreload=args.autoreload)
    if debug:
        application.listen(port)
    else:
        server = HTTPServer(application)
        server.bind(port)
        server.start(cpu_count)

    IOLoop().instance().start()


parser = argparse.ArgumentParser()
commands = parser.add_subparsers()

createproject_parser = commands.add_parser("createproject")
createproject_parser.add_argument("dir", default="", nargs="?")
createproject_parser.set_defaults(func=createproject)

createdockerfile_parser = commands.add_parser("createdockerfile")
createdockerfile_parser.add_argument("dir", default="", nargs="?")
createdockerfile_parser.add_argument("--encoding", default="utf-8")
createdockerfile_parser.set_defaults(func=createdockerfile)

runserver_parser = commands.add_parser("runserver")
runserver_parser.add_argument("-A", "--app")
runserver_parser.add_argument("--debug", action="store_true")
runserver_parser.add_argument("--autoreload", action="store_true")
runserver_parser.set_defaults(func=runserver)

runworker_parser = commands.add_parser("runworker")
runworker_parser.add_argument("-A", "--app")
runworker_parser.set_defaults(func=runworker)

proccess_parser = commands.add_parser("proccess")
proccess_parser.add_argument("cmd", default="", nargs="?")
proccess_parser.add_argument("filename")
proccess_parser.add_argument("-A", "--app")
proccess_parser.add_argument("--content-type")
proccess_parser.set_defaults(func=proccess)


def main():
    args, unknown = parser.parse_known_args()
    if hasattr(args, "func"):
        args.func(args, unknown)
    else:
        parser.print_help()


if "__main__" == __name__:
    main()
