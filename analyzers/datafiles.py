#!/usr/bin/env python3

# Extract Possible IoC of package
# -*- coding: utf-8 -*-

# %%%%%%%%%%% Libraries %%%%%%%%%%%#

import re
import os
import gzip
import json
import magic
import codecs
import shutil
import tarfile
import iocextract
from auxiliar_functions.globals import tmp
from auxiliar_functions.globals import sandbox
from auxiliar_functions.globals import extensions
from auxiliar_functions.globals import magics_extension_allowed

# %%%%%%%%%%% Functions %%%%%%%%%%%#


def extract_data(path_pack, files, pkg_hashid):
    try:
        utf8read = codecs.getreader('utf-8')
        args = dict(pkg_hashid=pkg_hashid, name=path_pack,
                    urls=[], hashs=[], ips=[], emails=[])

        if re.search(".whl$", path_pack):
            for filename in files.namelist():
                # Extract exe, dll, etc. archivos "sospechosos" dentro del pkg
                # # Falta validar diversos filetype, regex o tupla
                # extensions = ['.exe','.sh','.c','.cc','
                # .bin','.dll','.rst','.sh','.pdb','.json']
                magic_type = magic.from_buffer(files.open(filename).read())
                if not any(extension in magic_type
                           for extension in magics_extension_allowed):
                    files.extract(filename, sandbox)
                with files.open(filename) as f:
                    content = f.read().decode('ISO-8859-1')
                    get_data(content,
                             filename,
                             path_pack,
                             pkg_hashid,
                             args)

        elif re.search(".tar.gz$", path_pack) or re.search(".tgz$", path_pack):
            for member in files.getmembers():
                f = utf8read(files.extractfile(member.name))

                try:
                    f_magic = utf8read(files.extractfile(member.name))
                    magic_type = magic.from_buffer(f_magic.read())
                    if not any(extension in magic_type
                               for extension in magics_extension_allowed):
                        files.extract(member.name, sandbox)
                except AttributeError:
                    pass
                except UnicodeDecodeError:
                    pass

                # Extract exe, dll, etc. archivos "sospechosos" dentro del pkg
                # Falta validar diversos filetype, regex o tupla
                # extensions = ['.exe','.sh','.c','.cc',
                # '.bin','.dll','.rst','.sh','.pdb','.json']
                try:
                    if any(member.name.rsplit('.', 1)[1] in i
                           for i in extensions):
                        content = f.read()
                        get_data(content,
                                 member.name,
                                 path_pack,
                                 pkg_hashid,
                                 args)
                except IndexError:
                    pass
        elif re.search('go_pkgs/\w+_-_\w+', path_pack):
            names = files.infolist()
            for file in names:
                content = files.read(file.filename).decode('ISO-8859-1')
                get_data(content,
                         file.filename,
                         path_pack,
                         pkg_hashid,
                         args)
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
                                    f = utf8read(
                                        tarcont.extractfile(member.name))
                                    content = f.read()
                                    get_data(content,
                                             member.name,
                                             path_pack,
                                             pkg_hashid,
                                             args)
                if re.search('.gz$', gemcont):
                    try:
                        with gzip.open(gemcont, 'rb') as f_magic:
                            magic_type = magic.from_buffer(f_magic.read())
                            if not any(extension in magic_type
                                       for extension in
                                       magics_extension_allowed):
                                files.extract(gemcont.split('/')[-1], sandbox)
                    except (AttributeError, KeyError):
                        pass

                    with gzip.open(gemcont, 'rb') as f:
                        content = f.read().decode('ISO-8859-1')
                        get_data(content,
                                 gemcont.rsplit(os.sep, 1)[1],
                                 path_pack,
                                 pkg_hashid,
                                 args)

            shutil.rmtree(tmp + os.sep +
                          path_pack.rsplit(os.sep, 1)[1].rsplit('.', 1)[0])

        args['emails'] = sorted(args['emails'])

        return json.dumps(args)
    except:
        return json.dumps('[]')


def get_data(content, filename, path_pack, pkg_hashid, args):
    urls = set()
    hashs = set()
    ips = set()
    emails = set()

    for ci_urls in iocextract.extract_urls(content):
        urls.add(ci_urls)
    for ci_hash in iocextract.extract_hashes(content):
        hashs.add(ci_hash)
    for ci_ips in iocextract.extract_ips(content):
        ips.add(ci_ips)
    for ci_emails in iocextract.extract_emails(content):
        emails.add(ci_emails)
    data = dict(urls=list(urls), hashs=list(hashs),
                ips=list(ips), emails=list(emails))

    filename = filename.replace(".", "-")
    if len(urls) > 0:
        args['urls'] += data['urls']
    if len(hashs) > 0:
        args['hashs'] += data['hashs']
    if len(ips) > 0:
        args['ips'] += data['ips']
    if len(emails) > 0:
        args['emails'] += data['emails']

# %%%%%%%%%% The End %%%%%%%%%%#
