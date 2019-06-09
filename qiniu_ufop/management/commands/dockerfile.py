# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os
import sys

import qiniu_ufop
from ..base import BaseCommand


class Command(BaseCommand):
    def execute(self, args, unknown):
        datadir = os.path.join(os.path.dirname(qiniu_ufop.__file__), "data")
        dockerfile = os.path.join(datadir, "Dockerfile")
        with open(dockerfile, "r", encoding="utf-8") as f:
            sys.stdout.buffer.write(f.read().encode(args.encoding))

    def add_arguments(self):
        self.parser.add_argument("--encoding", default="utf-8")
