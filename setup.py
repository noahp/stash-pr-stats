#!/usr/bin/env python
"""
Setup package.
"""
from setuptools import setup

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
        "tqdm",
    ],
    entry_points={
        "console_scripts": ["stash-pr-stats=stash_pr_stats.stash_pr_stats:main"]
    },
)
