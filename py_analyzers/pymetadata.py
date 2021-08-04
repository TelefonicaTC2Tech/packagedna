#!/usr/bin/env python3

# Analyze Metadata PyPi

# %%%%%%%%%%% Libraries %%%%%%%%%%%#


import re
import json
import codecs
import datetime
import urllib.request
from pathlib import Path
from auxiliar_functions.globals import values
from auxiliar_functions.globals import meta_pack
from auxiliar_functions.globals import url_py_versions


def py_metadata(path_pack, files, pack_name, pkg_hashid, pkg_local):
    if pkg_local:
        return py_metadata_local(path_pack, files, pkg_hashid, pack_name)
    else:
        return py_metadata_net(path_pack, pack_name, pkg_hashid)


def py_metadata_local(path_pack, files, pkg_hashid, pack_name):
    try:
        utf8read = codecs.getreader('utf-8')
        metadata_pack = meta_pack
        if re.search(".whl$", path_pack):
            for info in files.infolist():
                if "METADATA" in info.filename:
                    member = info.filename
                    date = str(datetime.datetime(*info.date_time)
                               .isoformat()).split('T')[0]
                    metadata_pack['Date:'] = date
                    cfg = utf8read(files.open(member))

                    for line in cfg.readlines():
                        for data in metadata_pack:
                            if data in line:
                                if metadata_pack[data] == "":
                                    metadata_pack = extract("whl",
                                                            metadata_pack,
                                                            data, line)
                            elif "Metadata-Version:" in line:
                                metadata_pack = extract("whl", metadata_pack,
                                                        'Version:',
                                                        line)
                            elif "Maintainer:" in line:
                                metadata_pack = extract("whl", metadata_pack,
                                                        'Author:',
                                                        line)
                            elif "Maintainer-email:" in line:
                                metadata_pack = extract("whl", metadata_pack,
                                                        'Author-email:', line)
                            elif "Home-page:" in line:
                                metadata_pack = extract("whl", metadata_pack,
                                                        'Home-page:', line)

        elif re.search(".tar.gz$", path_pack):
            for info in files.getmembers():
                if "setup.py" in info.name:
                    metadata_pack['Date:'] = str(datetime.datetime.
                                                 fromtimestamp(info.mtime).
                                                 isoformat()).split('T')[0]
                    cfg = utf8read(files.extractfile(info.name))
                    for line in cfg.readlines():
                        line = line.replace(' ', '')
                        if ("name=" in line) or ("\'name\':" in line):
                            metadata_pack = extract("gz",
                                                    metadata_pack,
                                                    "Name:", line)
                        elif ("version=" in line) or ("\'version\':" in line):
                            metadata_pack = extract("gz",
                                                    metadata_pack,
                                                    "Version:",
                                                    line)
                        elif ("license=" in line) or ("\'license\':" in line):
                            metadata_pack = extract("gz",
                                                    metadata_pack,
                                                    "License:",
                                                    line)
                        elif ("url=" in line) or ("\'url\':" in line):
                            metadata_pack = extract("gz", metadata_pack,
                                                    "Home-page:", line)
                        elif ("author=" in line) or ("\'author\':" in line):
                            metadata_pack = extract("gz", metadata_pack,
                                                    "Author:", line)
                        elif ("author_email=" in line) or \
                                ("\'author_email\':" in line):
                            metadata_pack = extract("gz", metadata_pack,
                                                    "Author-email:", line)
        metadata_found = {
            'pkg_hashid': pkg_hashid,
            'name': metadata_pack['Name:'],
            'path_pack': path_pack,
            'author': metadata_pack['Author:'],
            'author_email': metadata_pack['Author-email:'],
            'version': metadata_pack['Version:'],
            'date': metadata_pack['Date:'],
            'license': metadata_pack['License:'],
            'home_page': metadata_pack['Home-page:']
        }

        if not metadata_found['name']:
            metadata_found['name'] = pack_name

        return json.dumps(metadata_found)
    except:
        return json.dumps('[]')


def extract(org, metas_pack, key, line):
    if org == 'gz':
        if (line.find('= \"') != -1) or (line.find('= \'') != -1) or \
                (line.find(': \'') != -1):
            if line.find('= ') != -1:
                metas_pack[key] = line[line.find('= ') + 3:line.find(',') - 1]
            else:
                metas_pack[key] = line[line.find(': ') + 3:line.find(',') - 1]
        else:
            metas_pack[key] = line[line.find('=') + 2:line.find(',') - 1]

    else:
        try:
            if values.index(line[line.find(': ') + 2:line.find('\n')]) >= 0:
                metas_pack[key] = '<UNREGISTERED>'
        except ValueError:
            metas_pack[key] = line[line.find(': ') + 2:line.find('\n')]

    return metas_pack


def py_metadata_net(path_pack, pack_name, pkg_hashid):
    pack_version = extract_version(path_pack, pack_name)
    try:
        file_meta = json.loads(urllib.request.urlopen(
            url_py_versions + pack_name + '/' + pack_version + '/json')
                               .read().decode('utf-8'))
    except Exception:
        file_meta = json.loads(urllib.request.urlopen(
            url_py_versions + pack_name + '/json').read().decode('utf-8'))

    metadata_found = dict(pkg_hashid=pkg_hashid,
                          name=file_meta['info'].get('name', ""),
                          path_pack=path_pack,
                          author=file_meta['info'].get('author', ""),
                          author_email=file_meta['info'].get(
                              'author_email', ""),
                          version=pack_version)
    try:
        metadata_found['date'] = file_meta['releases'].get(
            metadata_found['version'])[0].get('upload_time', "")
    except Exception:
        metadata_found['date'] = ""
    metadata_found['license'] = file_meta['info'].get('license', "")
    metadata_found['home_page'] = file_meta['info'].get('home_page', "")

    return json.dumps(normalized_meta(metadata_found))


def normalized_meta(metadata_found):
    for key in list(metadata_found.keys()):
        if metadata_found[key] == "" or metadata_found[key] == "UNKNOWN":
            metadata_found[key] = '<UNREGISTERED>'

    return metadata_found


def extract_version(path_pack, pack_name):
    try:
        # path_pack = path_pack.lower().split(pack_name)[1]
        version = Path(path_pack).resolve().stem.split(
            pack_name)[1].split('-')[1]
    except IndexError:
        # path_pack = path_pack.lower().split(pack_name.replace('-', '_'))[1]
        try:
            version = Path(path_pack).resolve().stem.split(pack_name.replace(
                '-', '_'))[1].split('-')[1]
        except IndexError:
            version = Path(path_pack).resolve().stem.split(pack_name.replace(
                '-', '.'))[1].split('-')[1]
    except Exception:
        version = ""

    return version

# %%%%%%%%%% The End %%%%%%%%%%#
