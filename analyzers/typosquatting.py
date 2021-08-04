#!/usr/bin/env python3

# Detect possible typosquatting
# -*- coding: utf-8 -*-

# %%%%%%%%%%% Libraries %%%%%%%%%%%#

import json
import Levenshtein
import urllib.request
from tqdm import tqdm
from auxiliar_functions.globals import vowels
from auxiliar_functions.globals import url_py
from auxiliar_functions.globals import replace
from auxiliar_functions.globals import py_list
from auxiliar_functions.globals import rb_list
from auxiliar_functions.globals import addition
from auxiliar_functions.globals import npm_list
from auxiliar_functions.globals import keyboards
from auxiliar_functions.globals import select_url
from auxiliar_functions.globals import select_file
from auxiliar_functions.globals import substitution
from auxiliar_functions.globals import url_rb_list
from auxiliar_functions.globals import url_npm_list

from go_analyzers.golibrary import go_library
from py_analyzers.pylibrary import py_library
from rb_analyzers.rblibrary import rb_library
from npm_analyzers.npmlibrary import npm_library


# %%%%%%%%%%% Functions %%%%%%%%%%%#
def typos_create(packname, library):
    if packname.find('/') != -1:
        preresult = {}
        parts = packname.split('/')
        exclude = ['github.com', 'gopkg.in', 'k8s.io', 'go.opentelemetry.io',
                   'modernc.org', 'kubevirt.io', 'go.chromium.org',
                   'go.etcd.io', 'golang.org', 'v2ray.com',
                   'code.cloudfoundry.org']
        for part in parts:
            if (part in exclude) or (part[0] == '@'):
                preresult[parts.index(part)] = [part]
            else:
                preresult[parts.index(part)] = typo_generator(part, library)
        x = 1
        while len(parts) - x >= 1:
            res = []
            for i in preresult[len(preresult.keys()) - 2]:
                for j in preresult[len(preresult.keys()) - 1]:
                    res.append(i + '/' + j)

            preresult[len(preresult.keys()) - 2] = res
            preresult.pop(len(preresult.keys()) - 1)
            x += 1

        result = preresult[0]

    else:
        result = typo_generator(packname, library)

    return result


def typo_generator(packname, library):
    result = []
    for i in range(0, len(packname)):
        result.append(packname[:i] + '-' + packname[i:])
        result.append(packname[:i] + packname[i] + packname[i:])
        result.append(packname[:i] + packname[i + 1:])

        if i < len(packname) - 2:
            result.append(packname[:i] + packname[i + 1]
                          + packname[i] + packname[i + 2:])
        if i == len(packname) - 2:
            result.append(packname[:i] + packname[i + 1] + packname[i])

    result = keyboard(packname, result)
    result = additions(packname, result)
    result = sustitutions(packname, result)
    result = levenshtein(packname, result, library)

    result = sorted(list(set(result)))
    return result


def replaces(packname, result):
    for i in range(0, len(packname)):
        if packname[i].isalpha():
            result.append(
                packname[:i] + packname[i] + packname[i] + packname[i + 1:])
            if packname[i] in replace:
                for change in replace[packname[i]]:
                    result.append(packname[:i] + change + packname[i + 1:])

        for vowel in vowels:
            if packname[i] in vowel:
                result.append(packname[:i] + vowel + packname[i + 1:])

    return result


def additions(packname, result):
    for add in addition:
        result.append(packname + add)
        result.append(add + packname)
    return result


def sustitutions(packname, result):
    for substitute in substitution.keys():
        if packname.find(substitute) != -1:
            for changes in substitution[substitute]:
                result.append(packname.replace(substitute, changes))
    return result


def keyboard(packname, result):
    for i in range(0, len(packname)):
        for keys in keyboards:
            if packname[i] in keys:
                for c in keys[packname[i]]:
                    result.append(
                        packname[:i] + c + packname[i] + packname[i + 1:])
                    result.append(
                        packname[:i] + packname[i] + c + packname[i + 1:])
                    result.append(
                        packname[:i] + c + packname[i + 1:])

    return result


def levenshtein(packname, result, library):
    lev_sensibility_distance = 2
    if library == 'go':
        return result

    with open(select_file[library]) as packages:
        for package in packages.readlines():
            package = package.split('\n')[0]
            if Levenshtein.distance(packname, package)\
                    <= lev_sensibility_distance:
                result.append(package)

    return result


def py_packages_list():
    py_packs = []
    for name in urllib.request.urlopen(url_py).readlines():
        if b'href' in name:
            extract = str(name)
            py_packs.append(extract[
                           extract.find('simple/') + 7:
                           extract.find('/', extract.find('simple/') + 7)])
    return py_packs


def rb_packages_list():
    res = urllib.request.urlopen(url_rb_list).read().decode('utf-8')
    rb_packs = res.split('\n')

    return rb_packs


def npm_packages_list():
    npm_packs = []
    try:
        res = urllib.request.urlopen(url_npm_list)
        res_json = json.loads(res.read().decode('utf-8'))
        i = 0
        while i <= len(res_json['rows']):
            npm_packs.append(res_json['rows'][i]['id'])
            i += 1
    except:
        print('Error')

    return npm_packs


def create_files_list(name, list_packs):
    file = open(name, 'w')
    for pack in list_packs:
        file.write(pack)
        file.write('\n')
    file.close()


def update_files(library):
    if library == 'py':
        packs = py_packages_list()
        create_files_list(py_list, packs)
    if library == 'rb':
        packs = rb_packages_list()
        create_files_list(rb_list, packs)
    if library == 'npm':
        packs = npm_packages_list()
        create_files_list(npm_list, packs)


def typo_web(library, typo_combinations):
    typo_download_results = {}
    for typo in tqdm(typo_combinations, desc=' Searching Typosquatting ...'):
        libraries = {}
        typo_url = select_url[library] + typo
        if library == 'py':
            library_result = py_library(typo_url, libraries)
        elif library == 'rb':
            library_result = rb_library(typo_url, libraries)
        elif library == 'npm':
            library_result = npm_library(typo_url, libraries)
        elif library == 'go':
            library_result = go_library(typo_url, libraries)
        else:
            library_result = []
        if 'error' not in library_result:
            typo_download_results[typo] = typo_url
    typo_download_results = json.dumps(typo_download_results)
    return typo_download_results


def typo_local(library, typo_combinations):
    typo_download_results = {}
    if library == 'go':
        return typo_web(library, typo_combinations)
    for typo in tqdm(typo_combinations, desc=' Searching Typosquatting ...'):
        libraries = {}
        with open(select_file[library]) as packages:
            if typo in packages.read():
                typo_url = select_url[library] + typo
                if library == 'py':
                    library_result = py_library(typo_url, libraries)
                elif library == 'rb':
                    library_result = rb_library(typo_url, libraries)
                elif library == 'npm':
                    library_result = npm_library(typo_url, libraries)
                elif library == 'go':
                    library_result = go_library(typo_url, libraries)
                if 'error' not in library_result:
                    typo_download_results[typo] = typo_url

    typo_download_results = json.dumps(typo_download_results)
    return typo_download_results
