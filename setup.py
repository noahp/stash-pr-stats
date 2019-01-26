#!/usr/bin/env python
"""
Setup package.
"""
from os import path
import sys
import os
from setuptools import setup

# conditionally insert extra requirements
INSTALL_CONDITIONAL_REQUIRES = []

if sys.version_info < (3, 4):
    # pathlib backport for forming uri's for paths
    INSTALL_CONDITIONAL_REQUIRES += ["pathlib"]


def get_long_description():
    """Fetch long description from README.md adjacent to this file"""
    this_directory = path.abspath(path.dirname(__file__))
    if sys.version_info < (3, 4):
        with open(path.join(this_directory, "README.md"), "r") as readmefile:
            desc = readmefile.read()
    else:
        print(os.listdir(this_directory))
        with open(
            path.join(this_directory, "README.md"), encoding="utf-8"
        ) as readmefile:
            desc = readmefile.read()
    return desc


setup(
    name="stash-pr-stats",
    version="0.0.5",
    description="Get pr stats from stash (bitbucket server)",
    author="Noah Pendleton",
    author_email="2538614+noahp@users.noreply.github.com",
    url="https://github.com/noahp/stash-pr-stats",
    long_description=get_long_description(),
    long_description_content_type="text/markdown",
    packages=["stash_pr_stats"],
    # need an unreleased version of stashy for token support
    install_requires=["click", "pygal", "stashy==0.6", "tabulate", "tqdm"]
    + INSTALL_CONDITIONAL_REQUIRES,
    entry_points={
        "console_scripts": ["stash-pr-stats=stash_pr_stats.stash_pr_stats:main"]
    },
    # For scripts, this corrects shebang replacement, from:
    #  https://github.com/pybuilder/pybuilder/issues/168
    options={"build_scripts": {"executable": "/usr/bin/env python"}},
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.6",
        "Operating System :: OS Independent",
    ],
)
