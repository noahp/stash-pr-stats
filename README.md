[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg?style=for-the-badge)](https://github.com/ambv/black) [![Travis (.com) branch](https://img.shields.io/travis/com/noahp/stash-pr-stats/master.svg?style=for-the-badge)](https://travis-ci.com/noahp/stash-pr-stats) [![PyPI version](https://img.shields.io/pypi/v/stash-pr-stats.svg?longCache=true&style=for-the-badge)](https://pypi.org/project/stash-pr-stats/)
# stash-pr-stats
Simple wrapper around [stashy](https://github.com/cosmin/stashy) to pull stats
about PR's for users across repos in a project in bitbucket server (aka stash).

Prints PR stats summary (open + merged total) and generates an svg chart with
montly stats for selected users.

# install
```bash
pip install stash-pr-stats
```

# example usage
```bash
# see help for more options
stash-pr-stats --help

# running for a single user
stash-pr-stats --accesstoken <token> --searchuser noahp \
  --url="https://mystashserver.com"
+-------------+--------+----------+
| user        |   open |   merged |
+=============+========+==========+
| noahp       |      0 |      123 |
+-------------+--------+----------+
Success! see output file:///home/noah/dev/github/stash-pr-stats/pr-stats.svg
```
