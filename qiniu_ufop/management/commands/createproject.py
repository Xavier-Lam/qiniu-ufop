# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os
from shutil import copyfile

from ... import demo
from ..base import BaseCommand


class Command(BaseCommand):
    def execute(self, args, unknown):
        if args.dir and not os.path.exists(args.dir):
            os.makedirs(args.dir)

        copyfile(demo.__file__, os.path.join(args.dir, "app.py"))

        requirements = os.path.join(args.dir, "requirements.txt")
        if not os.path.exists(requirements):
            open(requirements, "a").close()

        envs = os.path.join(args.dir, ".env")
        if not os.path.exists(envs):
            with open(envs, "a") as f:
                f.writelines((
                    "# export your environments here\n",
                    "export C_FORCE_ROOT=1"
                ))

        datadir = os.path.join(os.path.dirname(demo.__file__), "data")
        supervisor_conf = "supervisor.conf"
        copyfile(
            os.path.join(datadir, supervisor_conf),
            os.path.join(args.dir, supervisor_conf))

    def add_arguments(self):
        self.parser.add_argument("dir", default="", nargs="?")
