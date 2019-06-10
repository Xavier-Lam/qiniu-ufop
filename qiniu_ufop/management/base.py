# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from argparse import ArgumentParser
import os
from pkgutil import iter_modules
import sys

from kombu.utils.imports import symbol_by_name
from kombu.utils.objects import cached_property

import qiniu_ufop


def find_commands(dir):
    command_dir = os.path.join(dir, "commands")
    return [
        name for _, name, is_pkg in iter_modules([command_dir])
        if not is_pkg and not name.startswith('_')]


class CommandParser(ArgumentParser):
    @cached_property
    def parsers(self):
        return self.add_subparsers()

    @cached_property
    def commands(self):
        rv = dict()
        dir = os.path.dirname(__file__)
        command_names = find_commands(dir)
        for name in command_names:
            cls = symbol_by_name(
                "qiniu_ufop.management.commands.%s:Command" % name)
            parser = self.parsers.add_parser(
                name, help=cls.__doc__, description=cls.__doc__)
            parser.root = self
            cmd = cls(parser)
            rv[name] = cmd
        return rv

    def execute_from_command_line(self, argv=None):
        argv = argv or sys.argv[1:]
        self.commands
        args, unknown = self.parse_known_args(argv)
        if hasattr(args, "execute"):
            args.execute(args, unknown)
        else:
            self.print_help()


class BaseCommand(object):
    def __init__(self, parser):
        """
        :type parser: argparse.ArgumentParser
        """
        parser.set_defaults(execute=self.execute)
        self.parser = parser
        self.add_arguments()

    def add_arguments(self):
        pass

    def execute(self, args, unknown):
        raise NotImplementedError()
