#!/usr/bin/env python3

# Extract hash files of package
# -*- coding: utf-8 -*-

# %%%%%%%%%%% Libraries %%%%%%%%%%%#


import re
import os
import json
import gzip
import shutil
import hashlib
import tarfile

from auxiliar_functions.globals import tmp


# %%%%%%%%%%% Functions %%%%%%%%%%%#


def get_hash_pkg(path_pack):
    with open(path_pack, "rb") as f:
        f_bytes = f.read()  # read entire file as bytes
        pkg_sha256 = hashlib.sha256(f_bytes).hexdigest()
    return pkg_sha256


def hash_files(path_pack, pkg_hashid, files):
    hashes_data = {}
    hashes_data.update({'pkg_hashid': pkg_hashid})
    if re.search(".whl$", path_pack):
        for filename in files.namelist():
            with files.open(filename) as f:
                content = f.read()
                sha256 = hashlib.sha256(content).hexdigest()
                hashes_data.update({filename.replace(".", "-"): sha256})

    elif re.search(".tar.gz$|.tgz$", path_pack):
        for member in files.getmembers():
            try:
                content = files.extractfile(member).read()
            except:
                continue
            sha256 = hashlib.sha256(content).hexdigest()
            hashes_data.update({member.name.replace(".", "-"): sha256})

    elif re.search(".gem$", path_pack):
        with tarfile.open(path_pack) as gema:
            gema.extractall(tmp + os.sep +
                            path_pack.rsplit(os.sep, 1)[1].rsplit('.', 1)[0])

        for gemcont in os.listdir(tmp + os.sep +
                                  path_pack.rsplit(os.sep, 1)[1]
                                           .rsplit('.', 1)[0]):
            gemcont = tmp + os.sep + \
                      path_pack.rsplit(os.sep, 1)[1].rsplit('.', 1)[0] + \
                      os.sep + gemcont
            if re.search('.tar.gz$', gemcont):
                with tarfile.open(gemcont) as tarcont:
                    for member in tarcont.getmembers():
                        try:
                            content = files.extractfile(member).read()
                        except:
                            continue
                        sha256 = hashlib.sha256(content).hexdigest()
                        hashes_data.update(
                            {member.name.replace(".", "-"): sha256}
                            )

            if re.search('.gz$', gemcont):
                with gzip.open(gemcont, 'rb') as f:
                    content = f.read()
                    sha256 = hashlib.sha256(content).hexdigest()
                    hashes_data.update({gemcont.replace(".", "-"): sha256})

        shutil.rmtree(tmp + os.sep +
                      path_pack.rsplit(os.sep, 1)[1].rsplit('.', 1)[0])
    elif re.search('go_pkgs/\w+_-_\w+', path_pack):
        names = files.infolist()
        for file in names:
            content = files.read(file.filename)
            sha256 = hashlib.sha256(content).hexdigest()
            hashes_data.update({file.filename.replace(".", "-"): sha256})

    hashes_data = json.dumps(hashes_data)
    return hashes_data


# %%%%%%%%%% The End %%%%%%%%%%#
