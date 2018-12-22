#!/usr/bin/env python
"""
Setup package.
"""
import sys
from setuptools import setup


# conditionally insert extra requirements
INSTALL_CONDITIONAL_REQUIRES = []

if sys.version_info < (3, 4):
    # pathlib backport for forming uri's for paths
    INSTALL_CONDITIONAL_REQUIRES += ["pathlib"]


setup(
    name="stash-pr-stats",
    version="0.0.0",
    description="Get pr stats from stash (bitbucket server)",
    author="noahp",
    author_email="none",
    url="https://github.com/noahp/stash-pr-stats",
    packages=["stash_pr_stats"],
    # need an unreleased version of stashy for token support
    install_requires=[
        "click",
        "pygal",
        "stashy @ git+https://github.com/noahp/stashy.git@f42707cb87fe7a50f77d739b00494720062fd06e",
        "tabulate",
        "tqdm",
    ]
    + INSTALL_CONDITIONAL_REQUIRES,
    entry_points={
        "console_scripts": ["stash-pr-stats=stash_pr_stats.stash_pr_stats:main"]
    },
)
