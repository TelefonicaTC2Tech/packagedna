#!/usr/bin/env python3

# Analyze PyPI Library

# %%%%%%%%%%% Libraries %%%%%%%%%%%#
import json
import urllib.request

from auxiliar_functions.globals import url_py_versions
# %%%%%%%%%%% Functions %%%%%%%%%%%#


def py_library(url, libraries, specific_version=None):
    library = url.split('/')[4]
    try:
        urllib.request.urlopen(url)
    except:
        libraries['error'] = 'error'
        libraries = json.dumps(libraries)
        return libraries
    try:
        url = url_py_versions + library + '/json'
        py_json = json.loads(
            urllib.request.urlopen(url).read().decode('utf-8'))
        libraries[library] = {}
        if specific_version:
            return json.dumps({library: {
                specific_version: [py_json['releases'][
                                       specific_version][0]['url'],
                                   py_json['releases'][
                                       specific_version][0]['digests'][
                                       'sha256']]}})
        for ver in list(py_json['releases'].keys()):
            try:
                libraries[library][ver] = \
                    [py_json['releases'][ver][0]['url'],
                     py_json['releases'][ver][0]['digests']['sha256']]
            except:
                pass
        if not libraries[library]:
            raise ValueError
    except:
        libraries.clear()
        libraries['error'] = 'error'
        libraries = json.dumps(libraries)
        return libraries

    return json.dumps(libraries)

# %%%%%%%%%% The End %%%%%%%%%%#
