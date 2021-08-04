#!/usr/bin/env python3

# Analyze Metadata Ruby Gems

# %%%%%%%%%%% Libraries %%%%%%%%%%%#

import os
import json
import gzip
import urllib.request
from auxiliar_functions.globals import url_rb
from auxiliar_functions.globals import values
from auxiliar_functions.globals import meta_pack
from auxiliar_functions.globals import url_rb_versions

# %%%%%%%%%%% Functions %%%%%%%%%%%#


def rb_metadata(path_pack, pkg_hashid, files, local, pack_name):
    if local:
        return rb_metadata_local(path_pack, pkg_hashid, files)
    else:
        return rb_metadata_net(path_pack, pkg_hashid)


def rb_metadata_net(path_pack, pkg_hashid):
    metadata_pack = meta_pack
    keys = list(metadata_pack.keys())
    pack = path_pack[path_pack.rfind('/')+1:path_pack.rfind('-')]
    pack_version = path_pack[path_pack.rfind('-')+1:-4]
    file_meta = json.loads(urllib.request.urlopen(
        url_rb_versions + pack + '.json').read().decode('utf-8'))
    ver = 0
    while ver < len(file_meta):
        if file_meta[ver]['number'] == pack_version:
            for key in keys:
                if key == keys[0]:
                    metadata_pack[keys[0]] = pack
                elif key == keys[3]:
                    metadata_pack[keys[3]] = url_rb + '/' + pack
                elif key == keys[5]:
                    metadata_pack[keys[5]] = '<UNREGISTERED>'
                else:
                    metadata_pack[key] = normalized_meta(
                        metadata_pack, file_meta, ver, key)

            metadata_found = dict(pkg_hashid=pkg_hashid,
                                  name=metadata_pack['Name:'],
                                  path_pack=path_pack,
                                  author=metadata_pack['Author:'],
                                  author_email=metadata_pack['Author-email:'],
                                  version=metadata_pack['Version:'],
                                  date=metadata_pack['Date:'],
                                  license=metadata_pack['License:'],
                                  home_page=metadata_pack['Home-page:'])
            return json.dumps(metadata_found)

        ver += 1


def normalized_meta(metadata_pack, file_meta, i, key):
    data = ''
    if key == 'Author:':
        data = 'authors'
    elif key == 'Version:':
        data = 'number'
    elif key == 'Date:':
        data = 'built_at'
    elif key == 'License:':
        data = 'licenses'

    if file_meta[i][data] == "" or file_meta[i][data] == []:
        metadata = '<UNREGISTERED>'
    elif data == 'licenses':
        try:
            metadata = file_meta[i][data][0]
        except TypeError:
            metadata = ''

    else:
        metadata = file_meta[i][data]

    return metadata


def rb_metadata_local(path_pack, pkg_hashid, files):
    keys = list(meta_pack.keys())
    file_meta = 'metadata.gz'
    files.extract(file_meta)
    mail = 0
    aut = 0
    lic = 0
    with gzip.open(file_meta) as meta:
        for line in meta:
            line = str(line)
            if "name: " in line and meta_pack[keys[0]] == "":
                meta_pack[keys[0]] = line[line.find(': ') + 2:-3]
            if "  version:" in line and meta_pack[keys[1]] == "":
                meta_pack[keys[1]] = line[line.find(': ') + 2:-3]
            if "email:" in line:
                mail = 1
                if len(line) > 11:
                    meta_pack[keys[5]] = line[line.find(': ') + 2: - 3]
                    mail = 0
            if meta_pack[keys[5]] == "" and line.startswith('-', 2) \
                    and mail == 1:
                meta_pack[keys[5]] = line[line.find('- ') + 2: - 3]
            if "authors:" in line:
                aut = 1
            if meta_pack[keys[4]] == "" and line.startswith('-', 2) \
                    and aut == 1:
                meta_pack[keys[4]] = line[line.find('- ') + 2: - 3]
            if "licenses:" in line:
                lic = 1
                if len(line) > 14:
                    meta_pack[keys[2]] = line[line.find(': ') + 2: - 3]
            if meta_pack[keys[2]] == "" and line.startswith('-', 2) \
                    and lic == 1:
                meta_pack[keys[2]] = line[line.find('- ') + 2: - 3]
            if "homepage:" in line:
                meta_pack[keys[3]] = line[line.find(': ') + 2:-3]
            if "date:" in line:
                meta_pack[keys[6]] = line[line.find(': ') + 2:
                                          line.find(' 00:')]

    os.remove(file_meta)

    for x, y in meta_pack.items():
        if y in values:
            meta_pack[x] = '<UNREGISTERED>'
    metadata_found = dict(pkg_hashid=pkg_hashid,
                          name=meta_pack['Name:'],
                          path_pack=path_pack,
                          author=meta_pack['Author:'],
                          author_email=meta_pack['Author-email:'],
                          version=meta_pack['Version:'],
                          date=meta_pack['Date:'],
                          license=meta_pack['License:'],
                          home_page=meta_pack['Home-page:'])

    return json.dumps(metadata_found)

# %%%%%%%%%% The End %%%%%%%%%%#
