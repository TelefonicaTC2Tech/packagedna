#!/usr/bin/env python3

# Download PyPI Library

# %%%%%%%%%%% Libraries %%%%%%%%%%%#

import os
import json
import hashlib
import urllib.request

from tqdm import tqdm
from auxiliar_functions.globals import pypi_pkgs


# %%%%%%%%%%% Functions %%%%%%%%%%%#
from auxiliar_functions.messages import hashes_differences


def py_download(libraries):
    listsoft = []
    hashes = []
    soft = []
    path = pypi_pkgs + os.sep
    for library in libraries:
        for version in libraries[library]:
            listsoft.append(libraries[library][version][0])
            hashes.append(libraries[library][version][1][0:64])

    for url in tqdm(listsoft, desc=' Downloading packages...'):
        filename = url.split('/')[7]
        try:
            with urllib.request.urlopen(url) as resp, open(
                    path + filename.lower(), 'wb') as out:
                file = resp.read()
                out.write(file)
                hash_reported = hashes[listsoft.index(url)]
                hash_calculated = hashlib.sha256(file).hexdigest()
                if hash_reported != hash_calculated:
                    hashes_differences(path + filename, hash_reported,
                                       hash_calculated)
                soft.append(path + filename.lower())
        except:
            continue

    return json.dumps(soft)

# %%%%%%%%%% The End %%%%%%%%%%#
