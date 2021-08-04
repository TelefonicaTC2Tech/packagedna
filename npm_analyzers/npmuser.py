#!/usr/bin/env python3

# Detect libraries for user in PyPI

# %%%%%%%%%%% Libraries %%%%%%%%%%%#
import json
import urllib.request

from parsel import Selector
from auxiliar_functions.globals import url_npm_user


# %%%%%%%%%%% Functions %%%%%%%%%%%#


def npm_user(username):
    user_npm = {}
    try:
        sel = Selector(
            text=str(urllib.request.urlopen(url_npm_user + username).
                     read()), type='html')

        user_npm['username'] = username

        name = sel.xpath(
            '//*[@id="main"]/div/div[1]/div[2]/div/div').get()
        if name is None:
            user_npm['name'] = '<UNREGISTERED>'
        else:
            user_npm['name'] = name[name.find('2">') + 3:name.find('</div')]

        user_npm['yours_repositories'] = {}
        i = 1
        while i != 0:
            name_repo = sel.xpath('//*[@id="main"]/div/div[2]/div/div/ul/li['
                                  '' + str(i) + ']/section/div[1]/div[1]/a/h3'
                                  ).get()

            if name_repo is not None:
                name_repo = name_repo[
                                   name_repo.find('black">') + 7:
                                   name_repo.find('</h3>')]
                user_npm['yours_repositories'][name_repo] = {}
                user_npm['yours_repositories'][name_repo]['language'] = 'NPM'
                user_npm['yours_repositories'][name_repo]['url'] = \
                    'https://www.npmjs.com/package/' + name_repo
                i += 1
            else:
                i = 0

    except:
        pass

    return json.dumps(user_npm)
