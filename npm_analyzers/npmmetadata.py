import os
import json
import shutil
import datetime

from auxiliar_functions.globals import tmp
from auxiliar_functions.globals import meta_pack


def npm_metadata(path_pack, pkg_hashid, files, pack_name):

    metadata_pack = meta_pack

    for info in files.getmembers():
        if info.name.find('package.json') != -1:
            files.extract(info.name, tmp)
            file_meta = tmp + os.sep + info.name

    metadata_pack['Date:'] = datetime.datetime.fromtimestamp(
        os.path.getmtime(file_meta)).isoformat().split('T')[0]

    with open(file_meta) as file:
        data = json.load(file)
    try:
        metadata_pack['Name:'] = data['name']
    except (TypeError, KeyError):
        metadata_pack['Name:'] = ''

    try:
        metadata_pack['Version:'] = data['version']
    except (TypeError, KeyError):
        metadata_pack['Version:'] = ''

    if 'homepage' in list(data.keys()):
        try:
            metadata_pack['Home-page:'] = data['homepage']
        except (TypeError, KeyError):
            metadata_pack['Home-page:'] = ''

    if 'repository' in list(data.keys()):
        try:
            metadata_pack['Home-page:'] = data['repository']['url']
        except (TypeError, KeyError):
            metadata_pack['Home-page:'] = ''

    if 'license' in list(data.keys()):
        try:
            metadata_pack['License:'] = data['license']
        except (TypeError, KeyError):
            metadata_pack['License:'] = ''

    if 'licenses' in list(data.keys()):
        try:
            metadata_pack['License:'] = data['licenses'][0]['type']
        except TypeError:
            metadata_pack['License:'] = data['licenses'][0]
    try:
        author_data = data['author']
    except KeyError:
        author_data = ''
    if author_data != '':
        try:
            metadata_pack['Author:'] = author_data[:author_data.find(' <')]

            if author_data[author_data.find(' <')] != -1:
                metadata_pack['Author-email:'] = author_data[
                                                author_data.find(' <') + 2:
                                                author_data.find('> ')]
            else:
                metadata_pack['Author-email:'] = ''
        except AttributeError:
            try:
                metadata_pack['Author:'] = author_data['name']
            except KeyError:
                metadata_pack['Author:'] = ''
            try:
                metadata_pack['Author-email:'] = author_data['url']
            except KeyError:
                metadata_pack['Author-email:'] = ""

    for key in list(metadata_pack.keys()):
        if metadata_pack[key] == '':
            metadata_pack[key] = '<UNREGISTERED>'

    metadata_found = dict(pkg_hashid=pkg_hashid, name=metadata_pack['Name:'],
                          path_pack=path_pack, author=metadata_pack['Author:'],
                          author_email=metadata_pack['Author-email:'],
                          version=metadata_pack['Version:'],
                          date=metadata_pack['Date:'],
                          license=metadata_pack['License:'],
                          home_page=metadata_pack['Home-page:'])
    try:
        shutil.rmtree(file_meta[:file_meta.find('package.json')])
    except:
        pass
    return json.dumps(metadata_found)
