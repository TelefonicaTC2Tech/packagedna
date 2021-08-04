#!/usr/bin/env python3

# Analyze Metadata GitHub

# %%%%%%%%%%% Libraries %%%%%%%%%%%#

import json
import urllib.request

from auxiliar_functions.globals import url_git


def git_metadata(path_pack, files, pack_name, pkg_hashid, pkg_local):
    version = path_pack.rsplit('_--_', 1)[1]

    try:
        tags = json.loads(urllib.request.urlopen(url_git + pack_name + '/tags')
                          .read().decode('utf-8'))
        for tag in tags:
            if tag['name'] == version:
                id_commit = tag['commit']['sha']
                break

        ver_info = json.loads(urllib.request.urlopen(
            url_git + pack_name + '/commits/' + id_commit).read()
                              .decode('utf-8'))

        metadata_found = dict(pkg_hashid=pkg_hashid, name=pack_name,
                              path_pack=path_pack,
                              author=ver_info['commit']['author']['name'],
                              author_email=ver_info['commit']['author'][
                                  'email'], version=version,
                              date=ver_info['commit']['author']['date'])
    except:
        metadata_found = {}

    return json.dumps(metadata_found)

# %%%%%%%%%% The End %%%%%%%%%%#
