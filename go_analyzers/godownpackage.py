#!/usr/bin/env python3

# Download GO Library

# %%%%%%%%%%% Libraries %%%%%%%%%%%#

import os
import json
import hashlib
import urllib.request

from tqdm import tqdm
from auxiliar_functions.globals import go_pkgs
from auxiliar_functions.messages import hashes_differences

# %%%%%%%%%%% Functions %%%%%%%%%%%#


def go_download(libraries):
    listsoft = []
    hashes = []
    soft = []
    path = go_pkgs + os.sep
    for library in libraries:
        for version in libraries[library]:
            listsoft.append(libraries[library][version][0])
            hashes.append(libraries[library][version][1][0:64])
    # listsoft = listsoft[:5]
    for url in tqdm(listsoft, desc=' Downloading packages...'):
        """repo = url.split('/', 3)[2]
        pack = url.split('/', 3)[3]

        if 'github.com' in repo:
            try:
                repo_info = json.loads(urllib.request.urlopen(url_git + pack)
                                       .read().decode('utf-8'))
                Repo.clone_from(repo_info['git_url'], go_pkgs + os.sep + pack)
                soft.append(path + pack)
            except:
                continue
        else:
            continue"""
        try:
            filename = library.replace('/', '_-_').lower() + '_-_' \
                       + url.rsplit('/', 1)[1]
            with urllib.request.urlopen(url) as resp, open(path + filename,
                                                           'wb') as out:
                file = resp.read()
                out.write(file)

            hash_reported = hashes[listsoft.index(url)]
            hash_calculated = hashlib.sha256(file).hexdigest()
            if hash_reported != hash_calculated:
                hashes_differences(path + filename, hash_reported,
                                   hash_calculated)
            soft.append(path + filename)
        except:
            continue

    return json.dumps(soft)

# %%%%%%%%%% The End %%%%%%%%%%#
