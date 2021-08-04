#!/usr/bin/env python3

# Download Git Library

# %%%%%%%%%%% Libraries %%%%%%%%%%%#

import os
import json
import urllib.request

from tqdm import tqdm
from auxiliar_functions.globals import git_pkgs


# %%%%%%%%%%% Functions %%%%%%%%%%%#


def git_download(libraries):
    listsoft = []
    hashes = []
    soft = []
    path = git_pkgs + os.sep
    for library in libraries:
        for version in libraries[library]:
            listsoft.append(libraries[library][version][0])
            hashes.append(libraries[library][version][1][0:64])

    for url in tqdm(listsoft, desc=' Downloading packages...'):
        try:
            filename = url[url.find('repos/') + 6:
                           url.find('/zipball')].replace(
                '/', '_-_') + '_--_' + url.rsplit('/', 1)[1]
            with urllib.request.urlopen(url) as resp, open(path + filename,
                                                           'wb') as out:
                file = resp.read()
                out.write(file)
            soft.append(path + filename)
        except:
            continue

    return json.dumps(soft)

# %%%%%%%%%% The End %%%%%%%%%%#
