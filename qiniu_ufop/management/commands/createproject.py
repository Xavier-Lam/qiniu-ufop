# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os
from shutil import copyfile

from kombu.utils.objects import cached_property

import qiniu_ufop
from ..base import BaseCommand


class Command(BaseCommand):
    def execute(self, args, unknown):
        if args.dir and not os.path.exists(args.dir):
            os.makedirs(args.dir)

        self.copydata("demo.py", args.dir, "app.py")

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

        self.copydata("supervisor.conf", args.dir)
        self.copydata(".dockerignore", args.dir)

    def add_arguments(self):
        self.parser.add_argument("dir", default="", nargs="?")

    def copydata(self, filename, target_dir, targetname=""):
        targetname = targetname or filename
        return copyfile(
            os.path.join(self.datadir, filename),
            os.path.join(target_dir, targetname))

    @cached_property
    def datadir(self):
        return os.path.join(os.path.dirname(qiniu_ufop.__file__), "data")
