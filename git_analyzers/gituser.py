#!/usr/bin/env python3

# Detect repos of user en GIT

# %%%%%%%%%%% Libraries %%%%%%%%%%%#

import json
import urllib.request

from auxiliar_functions.globals import url_git_user


# %%%%%%%%%%% Functions %%%%%%%%%%%#


def git_user(username):
    try:
        user_info = json.loads(urllib.request.urlopen(url_git_user + username)
                           .read().decode('utf-8'))

        if 'login' in user_info.keys():
            user_git = {'username': username, 'name': user_info['name'],
                        'yours_repositories': {}}
            repos = json.loads(urllib.request.urlopen(
                url_git_user + username + '/repos').read().decode('utf-8'))
            for repo in repos:
                user_git['yours_repositories'][repo['name']] = {
                    'language': repo['language'], 'url': repo['html_url']}
        else:
            user_git = {}

    except:
        user_git = {}

    return json.dumps(user_git)


