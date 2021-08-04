#!/usr/bin/env python3

# Detect libraries for user in RubyGems

# %%%%%%%%%%% Libraries %%%%%%%%%%%#
import json
import urllib.request

from auxiliar_functions.globals import url_rb_user


# %%%%%%%%%%% Functions %%%%%%%%%%%#


def rb_user(username):
    user_rb = {}
    try:
        data_user = json.loads(urllib.request.urlopen(
            url_rb_user + username + '/gems.json').read().decode('utf-8'))

        user_rb['username'] = username
        user_rb['name'] = data_user[0]['authors']
        user_rb['yours_repositories'] = {}
        for key in data_user:
            user_rb['yours_repositories'][key['name']] = dict(
                language='Ruby', url=key['project_uri'])

        return json.dumps(user_rb)

    except:
        return json.dumps(user_rb)

# %%%%%%%%%%% End %%%%%%%%%%%#
