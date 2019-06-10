# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os
from distutils.dir_util import copy_tree

from kombu.utils.objects import cached_property

import qiniu_ufop
from ..base import BaseCommand


class Command(BaseCommand):
    """创建一个项目"""

    def execute(self, args, unknown):
        src = os.path.join(os.path.dirname(qiniu_ufop.__file__), "project")
        dst = args.dir
        if args.dir and not os.path.exists(dst):
            os.makedirs(dst)
        copy_tree(src, dst)
        requirements = os.path.join(dst, "requirements.txt")
        with open(requirements, "a") as f:
            f.writelines(["qiniu-ufop==%s" % qiniu_ufop.__version__])

    def add_arguments(self):
        self.parser.add_argument("dir", default="", nargs="?", help="文件夹")
