"""
Cli for fetching pr stats for Bitbucket Server.
"""
from __future__ import print_function
from collections import Counter
from datetime import date
import os
import pickle
import pathlib
import sys
import tqdm
import click
import stashy
import pygal
import tabulate


def print_bold(msg, color=None):
    """Use click to print bold and colored"""
    click.echo(click.style(msg, fg=color, bold=True))


def get_prs(url, searchuser, accesstoken, projectkey):
    """Fetch the PR data for this user"""
    print_bold("Fetching repos for {}...".format(searchuser), color="magenta")
    # At the moment, this package depends on a fork of the stashy package. See:
    # https://github.com/cosmin/stashy/issues/109
    # https://github.com/cosmin/stashy/pull/111
    stashy_package_error_help = """Whoops, might need to remove stashy, try:
    pip uninstall stashy -y; pip install stash-pr-stats --upgrade"""
    repos = {}
    try:
        stash = stashy.client.Stash(base_url=url, token=accesstoken)
    except TypeError:
        print_bold(stashy_package_error_help, color="red")
        sys.exit(-1)
    for repo in tqdm.tqdm(list(stash.projects[projectkey].repos)):
        prs_open = 0
        pr_merged_dates = Counter()
        prs = stash.projects[projectkey].repos[repo["slug"]].pull_requests
        try:
            prs_open += len(list(prs.all(author=searchuser)))
        except TypeError:
            print_bold(stashy_package_error_help, color="red")
            sys.exit(-1)
        for pull_request in prs.all(state="MERGED", author=searchuser):
            prtime = date.fromtimestamp(pull_request["updatedDate"] / 1000).isoformat()
            pr_merged_dates[prtime] += 1

        if prs_open > 0 or pr_merged_dates:
            repos[repo["slug"]] = {"open": prs_open, "merged": pr_merged_dates}

    return repos


def get_monthly_merged(user, url, accesstoken, projectkey, pickled=False):
    """Retrieve montly merged stats for one user"""
    picklefilename = "{}.pickle".format(user)

    # if pickle is enabled attempt to load data first
    if pickled and os.path.isfile(picklefilename):
        with open(picklefilename, "rb") as picklefile:
            repos = pickle.load(picklefile)
    else:
        repos = get_prs(url, user, accesstoken, projectkey)
        with open(picklefilename, "w") as picklefile:
            pickle.dump(repos, picklefile)

    # consolidate data from each repo
    total_open = 0
    total_merged = Counter()
    for repo in repos:
        total_open += repos[repo]["open"]
        total_merged += repos[repo]["merged"]

        # Print out this repos data
        # print("merged: {}".format(sum(repos[repo]["merged"].values())))
        # print("open: {}".format(repos[repo]["open"]))
        # print("repo: {}".format(repo))
        # for key in sorted(repos[repo]["merged"].iterkeys()):
        #     print("{} : {}".format(key, repos[repo]["merged"][key]))

    # bucket up merged pr's by month
    monthly_merged = Counter()
    for key in total_merged:
        monthly_merged[key[:7]] += total_merged[key]

    return total_open, sum(total_merged.values()), monthly_merged


def make_chart(user_stats, all_months, user_sum_stats):
    """Produce a line chart of user stats"""
    # add empty entries for user months with no merges
    user_stats_lists = {}
    for user in user_stats:
        empty_months = dict.fromkeys(all_months, None)
        empty_months.update(user_stats[user])
        user_stats[user] = empty_months
        user_stats_lists[user] = [
            (key, user_stats[user][key]) for key in sorted(user_stats[user])
        ]

    line_chart = pygal.Line(x_label_rotation=-90, legend_at_bottom=True)
    line_chart.title = "Monthly PR merges"
    line_chart.x_labels = all_months

    for user in sorted(user_stats_lists):
        line_chart.add(
            "{} - {}".format(user, user_sum_stats[user]["merged"]),
            [x[1] for x in user_stats_lists[user]],
        )

    line_chart.render_to_file("pr-stats.svg")

    click.echo(
        click.style(
            "Success! see output {}".format(
                pathlib.Path(os.path.abspath("pr-stats.svg")).as_uri()
            ),
            fg="green",
            bold=True,
        )
    )


@click.command()
@click.version_option()
@click.option(
    "--accesstoken",
    help="Bearer token for authenticating on bitbucket server",
    prompt=True,
)
@click.option("--url", "-u", help="Bitbucket server base url", required=True)
@click.option(
    "--searchuser", "-s", help="Users to search for stats", prompt=True, multiple=True
)
@click.option("--projectkey", "-p", help="Project key", default="FW")
@click.option("--pickled", "-i", help="Try to use pickled output", is_flag=True)
def main(url, searchuser, accesstoken, projectkey, pickled):
    """
    Fetch bitbucket server (aka stash) pr stats for specified users and
    output ascii summary + pygal chart
    """

    user_stats = {}
    user_sum_stats = {}
    all_months = Counter()
    for user in searchuser:
        user_open, user_merged, monthly_merged = get_monthly_merged(
            user, url, accesstoken, projectkey, pickled
        )
        user_stats[user] = dict(monthly_merged)
        user_sum_stats[user] = {"open": user_open, "merged": user_merged}
        all_months += monthly_merged

    # summary table
    table_data = []
    for user in sorted(user_sum_stats):
        table_data.append(
            [user, user_sum_stats[user]["open"], user_sum_stats[user]["merged"]]
        )

    print(tabulate.tabulate(table_data, ["user", "open", "merged"], tablefmt="grid"))

    make_chart(user_stats, sorted(all_months), user_sum_stats)


if __name__ == "__main__":
    main()  # pylint: disable=no-value-for-parameter
