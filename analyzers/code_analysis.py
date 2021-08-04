#!/usr/bin/env python3

# Extract Possible IoC of package
# -*- coding: utf-8 -*-

# %%%%%%%%%%% Libraries %%%%%%%%%%%#

import re
import os
import gzip
import json
import codecs
import shutil
import tarfile
from auxiliar_functions.globals import tmp
from auxiliar_functions.globals import extensions

# %%%%%%%%%%% Functions %%%%%%%%%%%#


def extract_data_code_extract(path_pack, files, pkg_hashid, code_extract):
    try:
        utf8read = codecs.getreader('utf-8')
        args = {}
        if re.search(".whl$", path_pack):
            for filename in files.namelist():
                with files.open(filename) as f:
                    content = f.read().decode('ISO-8859-1')
                    code_extract_found = analyse_code_extract(content,
                                                              code_extract)
                    if code_extract_found:
                        args['name'] = path_pack
                        args['filename'] = filename
                        args['code_extract'] = code_extract_found
        elif re.search(".tar.gz$", path_pack) or re.search(".tgz$", path_pack):
            for member in files.getmembers():
                f = utf8read(files.extractfile(member.name))
                try:
                    if any(member.name.rsplit('.', 1)[1] in i
                           for i in extensions):
                        content = f.read()
                        code_extract_found = analyse_code_extract(content,
                                                                  code_extract)
                        if code_extract_found:
                            args['name'] = path_pack
                            args['filename'] = member.name
                            args['code_extract'] = code_extract_found
                except IndexError:
                    pass
        elif re.search(".gem$", path_pack):
            with tarfile.open(path_pack) as gema:
                gema.extractall(tmp + os.sep +
                                path_pack.rsplit(
                                    os.sep, 1)[1].rsplit('.', 1)[0])

            for gemcont in os.listdir(tmp + os.sep +
                                      path_pack.rsplit(os.sep, 1)[1]
                                      .rsplit('.', 1)[0]):
                gemcont = tmp + os.sep + \
                          path_pack.rsplit(os.sep, 1)[1].rsplit('.', 1)[0] + \
                          os.sep + gemcont
                if re.search('.tar.gz$', gemcont):
                    with tarfile.open(gemcont) as tarcont:
                        for member in tarcont.getmembers():
                            if member.name.find('.') > 0:
                                t = member.name.rsplit('.', 1)[1]
                                if any(t in i for i in extensions):
                                    f = utf8read(tarcont.extractfile(
                                        member.name))
                                    content = f.read()
                                    code_extract_found = analyse_code_extract(
                                        content, code_extract)
                                    args[t] = code_extract_found
                                    if code_extract_found:
                                        args[t] = code_extract_found

                if re.search('.gz$', gemcont):
                    with gzip.open(gemcont, 'rb') as f:
                        content = f.read().decode('ISO-8859-1')
                        code_extract_found = analyse_code_extract(content,
                                                                  code_extract)
                        if code_extract_found:
                            args['name'] = path_pack
                            args['filename'] = 'filename'
                            args['code_extract'] = code_extract_found
            shutil.rmtree(tmp + os.sep +
                          path_pack.rsplit(os.sep, 1)[1].rsplit('.', 1)[0])
        try:
            for filename in files.namelist():
                with files.open(filename) as f:
                    content = f.read().decode('ISO-8859-1')
                    code_extract_found = analyse_code_extract(content,
                                                              code_extract)
                    if code_extract_found:
                        args['name'] = path_pack
                        args['filename'] = filename
                        args['code_extract'] = code_extract_found
        except:
            pass
        args = json.dumps(args)
        return args
    except:
        return json.dumps('[]')


def analyse_code_extract(content, code_extract):
    code_extract = code_extract.strip().replace(' ', '').lower()
    content = content.replace(' ', '').lower()
    if content.find(code_extract) != -1:
        code_extract_found = content[content.find(code_extract) - 50:
                                     content.find(code_extract) + len(
                                         code_extract) + 50]
        return code_extract_found
    else:
        return None

# %%%%%%%%%% The End %%%%%%%%%%#
