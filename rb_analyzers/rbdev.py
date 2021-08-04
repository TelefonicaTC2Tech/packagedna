#!/usr/bin/env python3

# Detect libraries for user in RubyGems

# %%%%%%%%%%% Libraries %%%%%%%%%%%#
import json
import urllib.request
from rb_analyzers.rbuser import rb_user
from auxiliar_functions.globals import url_rb_dev


def rb_dev(pack):
    owners = {}
    try:
        data = json.loads(urllib.request.urlopen(
            f'{url_rb_dev}{pack}/owners.json').read().decode('utf-8'))
        i = 0
        for key in data:
            owners[i] = json.loads(rb_user(key['handle']))
            i += 1
    except Exception:
        pass
    return json.dumps(owners)

# %%%%%%%%%% The End %%%%%%%%%%
