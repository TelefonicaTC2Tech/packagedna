#!/usr/bin/env python3

# Download JS Library

# %%%%%%%%%%% Libraries %%%%%%%%%%%#

import os
import json
import hashlib
import urllib.request

from tqdm import tqdm
from auxiliar_functions.globals import npm_pkgs

# %%%%%%%%%%% Functions %%%%%%%%%%%#
from auxiliar_functions.messages import hashes_differences


def npm_download(libraries):
    listsoft = []
    hashes = []
    soft = []
    path = npm_pkgs + os.sep

    for library in libraries:
        for version in libraries[library]:
            listsoft.append(libraries[library][version][0])
            hashes.append(libraries[library][version][1])

    listsoft = listsoft[-3:]

    for url in tqdm(listsoft, desc=' Downloading packages...'):
        try:
            filename = url.split('/')[5]
            with urllib.request.urlopen(url) as resp, open(path + filename,
                                                           'wb') as out:
                file = resp.read()
                out.write(file)
                hash_reported = hashes[listsoft.index(url)]
                hash_calculated = hashlib.sha1(file).hexdigest()
                if hash_reported == hash_calculated:
                    hashes_differences(path + filename, hash_reported,
                                       hash_calculated)
                soft.append(path + filename)
        except:
            continue

    soft = json.dumps(soft)
    return soft
