# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from qiniu_ufop.utils import cpu_count, get_worker_instance
from ..base import BaseCommand


class Command(BaseCommand):
    """运行worker"""

    def execute(self, args, unknown):
        app = get_worker_instance(args.app)
        app.worker_main(["worker"] + unknown + ["-c", str(cpu_count())])

    def add_arguments(self):
        self.parser.add_argument("-A", "--app")
