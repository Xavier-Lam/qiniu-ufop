# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from contextlib import contextmanager
import os
import re
import sys

from kombu.utils.imports import symbol_by_name
from tornado.process import cpu_count as _cpu_count


def cpu_count(fake=True):
    if os.getenv("CPU_COUNT"):
        return int(os.environ["CPU_COUNT"])
    elif os.getenv("FLAVOR"):
        match = re.search(r"^C(\d+)M(\d+)$", os.environ["FLAVOR"])
        if match:
            return int(match.group(1))
    return 1 if fake else _cpu_count()


@contextmanager
def redirect_stdout(new_target):
    old_target, sys.stdout = sys.stdout, new_target
    try:
        yield new_target
    finally:
        sys.stdout = old_target


def get_worker_instance(name=None):
    name = name or os.getenv("QINIU_UFOP_CELERY")
    if not name:
        #  app默认取当前工作路径的app.ufop
        sys.path.append(os.getcwd())
        name = "app.ufop"
    celery = symbol_by_name(name)
    return celery
