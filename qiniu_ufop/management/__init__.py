# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from qiniu_ufop.management.base import CommandParser


def main():
    parser = CommandParser()
    parser.execute_from_command_line()
