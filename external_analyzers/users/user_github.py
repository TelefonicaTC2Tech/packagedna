#!/usr/bin/env python3

# Detect possible users in libraries of code
# -*- coding: utf-8 -*-

# %%%%%%%%%%% Libraries %%%%%%%%%%%#

import json
import requests

from auxiliar_functions.globals import libraries
from auxiliar_functions.auxiliar_functions import get_libraries_io_api_key


# %%%%%%%%%%% Functions %%%%%%%%%%%#

def repositories(user, api_key):
    repo = {}
    resp_repo = requests.get(
        libraries + user + '/repositories?api_key=' + api_key, verify=False)
    if resp_repo.status_code == 404:
        return repo

    for data_repo in json.loads(resp_repo.text):
        name_repo = data_repo['full_name'].split('/')[1]
        repo[name_repo] = dict(language=data_repo['language'],
                               url='https://github.com/' + user + '/' +
                                   name_repo)

    return repo


def user_github(user):
    try:
        api_key = get_libraries_io_api_key()
        resp = requests.get(libraries + user + '?api_key=' + api_key,
                            verify=False)

        if resp.status_code == 404:
            user_gh = dict(username=user, status='not found')

        data_user = json.loads(resp.text)
        user_gh = dict(username=data_user['login'], name=data_user['name'],
                       created_at=data_user['created_at'],
                       email=data_user['email'], website=data_user['blog'],
                       location=data_user['location'],
                       company=data_user['company'],
                       yours_repositories=repositories(user, api_key))

    except:
        user_gh = dict(name=user, status='error libraries.io')

    return json.dumps(user_gh, ensure_ascii=False)
