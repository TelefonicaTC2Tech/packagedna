#!/usr/bin/env python3

# Detect developers on GIT's repo

# %%%%%%%%%%% Libraries %%%%%%%%%%%#

import json
import urllib.request

from git_analyzers.gituser import git_user
from auxiliar_functions.globals import url_git


# %%%%%%%%%%% Functions %%%%%%%%%%%#


def git_dev(packname):
    try:
        pack_info = json.loads(urllib.request.urlopen(
            url_git + packname + '/tags').read().decode('utf-8'))
        users = []

        for comm in pack_info:
            try:
                commit_info = json.loads(urllib.request.urlopen(
                    comm['commit']['url']).read().decode('utf-8'))

                if 'login' in commit_info['author'].keys():
                    users.append(commit_info['author']['login'])
            except:
                pass

        i = 0
        owners = {}
        users = sorted(list(set(users)))
        for user in users:
            owners[i] = json.loads(git_user(user))
            i += 1

    except:
        owners = {}

    return json.dumps(owners)


