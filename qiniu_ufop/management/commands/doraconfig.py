# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import sys

import yaml

from ..base import BaseCommand


class Command(BaseCommand):
    def execute(self, args, unknown):
        conf = dict(
            ufopname=args.name,
            verstr=args.version,
            image=args.tag,
            desc=args.desc,
            flavor=args.flavor,
            health_check=dict(
                path="/health",
                timeout=3
            ),
            env={
                "global": [dict(
                    key="FLAVOR",
                    value=args.flavor
                )]
            },
            log_file_paths=[
                "/var/log/server/",
                "/var/log/supervisor/",
                "/var/log/worker/",
            ]
        )
        yaml.add_representer(
            type(None),
            lambda self, _: self.represent_scalar("tag:yaml.org,2002:null", "")
        )
        yaml.dump(conf, sys.stdout, sort_keys=False)

    def add_arguments(self):
        self.parser.add_argument("-n", "--name", required=True)
        self.parser.add_argument("-t", "--tag", required=True)
        self.parser.add_argument("-v", "--version", required=True)
        self.parser.add_argument("--flavor", default="C1M1")
        self.parser.add_argument("--desc")
