#!/usr/bin/env python3

# Detect libraries for user in PyPi

# %%%%%%%%%%% Libraries %%%%%%%%%%%#
import json
import urllib.request

from parsel import Selector
from py_analyzers.pyuser import py_user
from auxiliar_functions.globals import url_py_dev


# %%%%%%%%%%% Functions %%%%%%%%%%%#


def py_dev(pack):
    owners = {}
    try:
        sel = Selector(
            text=str(urllib.request.urlopen(url_py_dev + pack).read()),
            type='html')
        for x in range(4, 7):
            section = sel.xpath(f'//*[@id="content"]/div[4]/div/div/div[1]/'
                                f'div[{x}]/h3').get()
            if section.find('Maintainers') != -1:
                way = f'//*[@id="content"]/div[4]/div/div/div[1]/div[{x}]'
                break

        i = 1
        while i != 0:
            name = sel.xpath(f'{way}/span[{str(i)}]/a/span[2]').get()

            if name is not None:
                name = name[
                       name.find('t">\\n          ') + 15:
                       name.find('\\n        </span>')]
                owners[i - 1] = {}
                owners[i - 1] = json.loads(py_user(name))
                i += 1
            else:
                i = 0

    except:
        pass

    return json.dumps(owners)
