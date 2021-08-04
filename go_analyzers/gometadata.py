#!/usr/bin/env python3

# Analyze Metadata Go

# %%%%%%%%%%% Libraries %%%%%%%%%%%#

import json
import urllib.request
from urllib.error import HTTPError

from auxiliar_functions.globals import url_git
from auxiliar_functions.messages import rate_limit_exceeded


def go_metadata(path_pack, files, pack_name, pkg_hashid, pkg_local):
    version = path_pack.rsplit('_-_', 1)[1]
    if pkg_local.find('github.com/') != -1:
        pack = pkg_local[pkg_local.find('github.com/') + 11::]
    else:
        pack = ''

    try:
        tags = json.loads(urllib.request.urlopen(url_git + pack + '/tags')
                          .read().decode('utf-8'))
        for tag in tags:
            if tag['name'] == version:
                id_commit = tag['commit']['sha']
                break

        ver_info = json.loads(urllib.request.urlopen(
            url_git + pack + '/commits/' + id_commit).read().decode('utf-8'))

        metadata_found = dict(pkg_hashid=pkg_hashid, name=pkg_local,
                              path_pack=path_pack,
                              author=ver_info['commit']['author']['name'],
                              author_email=ver_info['commit']['author']
                              ['email'], home_page='', version=version,
                              date=ver_info['commit']['author']['date'])
    except HTTPError:
        rate_limit_exceeded(url_git)
        metadata_found = dict(pkg_hashid=pkg_hashid, name=pkg_local,
                              path_pack=path_pack,
                              author="",
                              author_email="",
                              home_page='', version=version,
                              date="")
    except:
        metadata_found = {}

    return json.dumps(metadata_found)

# %%%%%%%%%% The End %%%%%%%%%%#
