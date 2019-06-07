# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os
import re

from setuptools import find_packages, setup

package = dict()

with open(os.path.join("qiniu_ufop", "__init__.py"), "r") as f:
    lines = f.readlines()
    for line in lines:
        match = re.match(r"(__\w+?__)\s*=\s*(.+)$", line)
        if match:
            package[match.group(1)] = eval(match.group(2))

with open("README.md", "rb") as f:
    long_description = f.read().decode("utf-8")

with open("requirements.txt") as f:
    requirements = [l for l in f.read().splitlines() if l]

setup(
    name=package["__title__"],
    version=package["__version__"],
    author=package["__author__"],
    author_email=package["__author_email__"],
    url=package["__url__"],
    packages=find_packages(),
    keywords=["qiniu", "ufop", "七牛"],
    description=package["__description__"],
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires=requirements,
    include_package_data=True,
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: MacOS",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: POSIX",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: Implementation :: CPython",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
        "Topic :: Software Development :: Libraries",
        "Topic :: Software Development :: Libraries :: Application Frameworks",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Utilities"
    ],
    entry_points = dict(
        console_scripts=[
            "qiniu-ufop = bin.manage:main"
        ],              
    ),
)
