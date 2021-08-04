#!/usr/bin/env python3

# Analyze Ruby Gems Library

# %%%%%%%%%%% Libraries %%%%%%%%%%%#
import json
import urllib.request
from auxiliar_functions.globals import url_rb_download
from auxiliar_functions.globals import url_rb_versions


# %%%%%%%%%%% Functions %%%%%%%%%%%#
def rb_library(url, libraries, specific_version=None):
    library = url.split('/')[4]
    try:
        urllib.request.urlopen(url)
    except:
        libraries['error'] = 'error'
        libraries = json.dumps(libraries)
        return libraries
    try:
        url = url_rb_versions + library + '.json'
        rb_json = json.loads(
            urllib.request.urlopen(url).read().decode('utf-8'))
        if specific_version:
            for pack in rb_json:
                if pack['number'] == specific_version:
                    return json.dumps({library: {
                        pack['number']: [
                            url_rb_download + library + '-' +
                            pack['number'] + '.gem', pack['sha']
                        ]
                    }})

            return json.dumps(
                libraries[library]

            )

        try:
            libraries[library] = {}
        except TypeError:
            libraries = json.loads(libraries)
            libraries[library] = {}
        ver = 0
        while ver < len(rb_json):
            libraries[library][rb_json[ver]['number']] = \
                [url_rb_download + library + '-' + rb_json[ver]['number']
                 + '.gem', rb_json[ver]['sha']]
            ver += 1
    except:
        try:
            libraries['error'] = 'error'
        except:
            libraries = json.loads(libraries)
            libraries['error'] = 'error'
        libraries = json.dumps(libraries)
        return libraries

    return json.dumps(libraries)

# %%%%%%%%%% The End %%%%%%%%%%#
