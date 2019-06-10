# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import qiniu_ufop
from qiniu_ufop.management.base import CommandParser


def main():
    parser = CommandParser(
        description="qiniu-ufop %s" % qiniu_ufop.__version__)
    parser.execute_from_command_line()
