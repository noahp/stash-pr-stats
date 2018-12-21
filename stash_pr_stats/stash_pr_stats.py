"""
Cli for fetching pr stats for Bitbucket Server.
"""
from __future__ import print_function
import click
import stashy
from collections import Counter
from datetime import date

def get_prs(url, searchuser, accesstoken, projectkey):
    """Fetch the PR data for this user"""
    repos = {}
    stash = stashy.client.Stash(base_url=url, token=accesstoken)
    for repo in stash.projects["FW"].repos:
        prs_open = 0
        pr_merged_dates = Counter()
        prs = stash.projects["FW"].repos[repo["slug"]].pull_requests
        prs_open += len(list(prs.all(author=searchuser)))

        for pr in prs.all(state="MERGED", author=searchuser):
            prtime = date.fromtimestamp(pr["updatedDate"]/1000).isoformat()
            pr_merged_dates[prtime] += 1

        repos[repo["slug"]] = {"open": prs_open, "merged": pr_merged_dates}

    return repos


import pickle

@click.command()
@click.version_option()
@click.option(
    "--accesstoken",
    help="Bearer token for authenticating on bitbucket server",
    prompt=True,
)
@click.option("--url", "-u", help="Bitbucket server base url", required=True)
@click.option("--searchuser", "-s", help="User to search for stats", prompt=True)
@click.option("--projectkey", "-p", help="Project key")
def main(url, searchuser, accesstoken, projectkey="FW"):
    """Cli entry point"""

    repos = get_prs(url, searchuser, accesstoken, projectkey)
    # with open("npendleton.pickle", "w") as picklefile:
    #     pickle.dump(repos, picklefile)

    # with open("npendleton.pickle", "rb") as picklefile:
    #     repos = pickle.load(picklefile)

    for repo in repos.iterkeys():
        print("repo: {}".format(repo))
        print("open: {}".format(repos[repo]["open"]))
        print("merged: {}".format(sum(repos[repo]["merged"].values())))
        for key in sorted(repos[repo]["merged"].iterkeys()):
            print("{} : {}".format(key, repos[repo]["merged"][key]))

if __name__ == "__main__":
    main()  # pylint: disable=no-value-for-parameter
