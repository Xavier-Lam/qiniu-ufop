# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os
import subprocess

from qiniu_ufop.utils import redirect_stdout
from ..base import BaseCommand


class Command(BaseCommand):
    """一键部署"""

    def execute(self, args, unknown):
        dir = os.path.abspath(args.dir)

        # 生成配置文件
        dorayaml = os.path.join(dir, "dora.yaml")
        print("create dora.yaml...")
        with open(dorayaml, "w") as f:
            with redirect_stdout(f):
                self.parser.root.commands["doraconfig"].execute(
                    args, unknown)

        # build
        print("build docker image...")
        self.run(["docker", "build", dir, "-t", args.tag])

        # 上载
        print("push docker image...")
        self.run(["qdoractl", "push", args.tag])

        # 发布
        print("release...")
        self.run(["qdoractl", "release", "--config", dir])

        print("success")

    def add_arguments(self):
        self.parser.add_argument("dir", default="", nargs="?", help="文件夹")
        self.parser.add_argument(
            "-n", "--name", required=True, help="自定义处理程序名")
        self.parser.add_argument("-t", "--tag", required=True)
        self.parser.add_argument(
            "-v", "--version", required=True, help="版本")
        self.parser.add_argument("--flavor", default="C1M1", help="配置")
        self.parser.add_argument("--desc", help="描述")

    def run(self, *args, **kwargs):
        with subprocess.Popen(*args, **kwargs) as p:
            try:
                stdout, stderr = p.communicate()
            except:
                p.kill()
                p.wait()
                raise
            retcode = p.poll()
            if retcode != 0:
                exit(retcode)
