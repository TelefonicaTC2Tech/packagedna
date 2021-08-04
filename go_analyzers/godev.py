#!/usr/bin/env python3

# Detect developers on Go's repo

# %%%%%%%%%%% Libraries %%%%%%%%%%%#

import json

from git_analyzers.gitdev import git_dev


# %%%%%%%%%%% Functions %%%%%%%%%%%#


def go_dev(packname):
    if packname.find('github.com/') != -1:
        return git_dev(packname[packname.find('github.com/') + 11::])
    else:
        dev = {}
        return json.dumps(dev)
