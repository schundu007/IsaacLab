# Copyright (c) 2022-2026, The Isaac Lab Project Developers (https://github.com/isaac-sim/IsaacLab/blob/main/CONTRIBUTORS.md).
# All rights reserved.
#
# SPDX-License-Identifier: BSD-3-Clause

import requests


class PR:
    def __init__(self, number, title, author, checks_passed):
        self.number = number
        self.title = title
        self.author = author
        self.checks_passed = checks_passed


def fetch_prs():
    repo_url = "https://api.github.com/repos/venmo/foundations-interview/pulls?state=all"
    response = requests.get(repo_url)
    if not response.ok:
        return []

    prs = []
    for pr_data in response.json():
        number = pr_data["number"]
        title = pr_data["title"]
        author = pr_data["user"]["login"]

        # Check CI status
        status_url = f"https://api.github.com/repos/venmo/foundations-interview/commits/{pr_data['head']['sha']}/status"
        status_response = requests.get(status_url)
        checks_passed = status_response.ok and status_response.json().get("state") == "success"

        prs.append(PR(number, title, author, checks_passed))

    return prs


prs = fetch_prs()
for pr in prs:
    symbol = "✓" if pr.checks_passed else "✗"
    print(f'{symbol} {pr.author}: #{pr.number} "{pr.title}"')
