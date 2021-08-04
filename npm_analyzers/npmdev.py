#!/usr/bin/env python3

# Detect libraries for user in NPM

# %%%%%%%%%%% Libraries %%%%%%%%%%%#
import json
import urllib.request
from npm_analyzers.npmuser import npm_user
from auxiliar_functions.globals import url_npm

# %%%%%%%%%%% Functions %%%%%%%%%%%#


def npm_dev(pack):
    owners = {}
    try:
        data = json.loads(urllib.request.urlopen(
            url_npm + pack).read().decode('utf-8'))
        i = 0
        for key in data['maintainers']:
            owners[i] = json.loads(npm_user(key['name']))
            i += 1
    except Exception:
        pass
    return json.dumps(owners)

# %%%%%%%%%% The End %%%%%%%%%%
