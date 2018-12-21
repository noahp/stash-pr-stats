# stash-pr-stats
Simple wrapper around [stashy](https://github.com/cosmin/stashy) to pull stats
about PR's for users across repos in a project in bitbucket server (aka stash).

# install
```bash
pip install . -U
```

# example usage
```bash
stash-pr-stats --accesstoken <token> --searchuser noahp \
  --url="https://mystashserver.com"
```
