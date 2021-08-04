#!/usr/bin/env python3

# Detect libraries for user in PyPI

# %%%%%%%%%%% Libraries %%%%%%%%%%%#
import json
import urllib.request

from parsel import Selector
from auxiliar_functions.globals import url_py_user


# %%%%%%%%%%% Functions %%%%%%%%%%%#


def py_user(username):
    user_py = {}
    try:
        sel = Selector(
            text=str(urllib.request.urlopen(url_py_user + username).read()),
            type='html')

        user_py['username'] = username
        name = sel.xpath(
            '//*[@id="content"]/div/div/div[1]/div/div/h1').get()

        if name is None:
            user_py['name'] = '<UNREGISTERED>'
        else:
            user_py['name'] = name[name.find('name">') + 6:name.find('</h1>')]

        user_py['yours_repositories'] = {}
        i = 1
        while i != 0:
            name_repo = sel.xpath('//*[@id="content"]/div/div/div[2]/div/a['
                                  + str(i) + ']/h3').get()

            if name_repo is not None:
                name_repo = name_repo[
                                   name_repo.find('title">') + 7:
                                   name_repo.find('</h3>')]
                user_py['yours_repositories'][name_repo] = dict(
                    language='Python', url=
                    'https://pypi.org/project/' + name_repo)
                i += 1
            else:
                i = 0

    except:
        pass

    return json.dumps(user_py)
