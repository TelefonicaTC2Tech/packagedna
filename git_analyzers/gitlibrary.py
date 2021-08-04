#!/usr/bin/env python3

# Analyze GitHub Repository

# %%%%%%%%%%% Libraries %%%%%%%%%%%#
import json
import urllib.request
import requests

from auxiliar_functions.auxiliar_functions import get_github_api_token
from auxiliar_functions.globals import url_git

# %%%%%%%%%%% Functions %%%%%%%%%%%#


def git_library(url, libraries, specific_version=None):
    repo = url.split('github.com/')[1]
    try:
        urllib.request.urlopen(url)
    except:
        libraries['error'] = 'error'
        return json.dumps(libraries)

    libraries[repo] = {}
    token = get_github_api_token()
    if token:
        headers = {
            "Authorization": "token {}".format(token),
            "Accept": "application/vnd.github.mercy-preview+json"
        }
    else:
        headers = {}

    response = requests.get(url_git + repo + '/tags',
                            headers=headers, verify=False)

    if response.status_code == 403:
        raise requests.HTTPError(response=403)

    for info in response.json():
        libraries[repo][info['name']] = [info['zipball_url'],
                                         info['commit']['sha']]

    return json.dumps(libraries)


