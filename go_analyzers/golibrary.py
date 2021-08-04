#!/usr/bin/env python3

# Analyze GO Library

# %%%%%%%%%%% Libraries %%%%%%%%%%%#
import json
import requests
import urllib.request

from parsel import Selector
from git_analyzers.gitlibrary import git_library

# %%%%%%%%%%% Functions %%%%%%%%%%%#


def go_library(url, libraries, specific_version=None):
    library = url.split('/', 3)[3]
    try:
        url_opened = urllib.request.urlopen(url)
    except:
        libraries['error'] = 'error'
        return json.dumps(libraries)

    libraries[library] = {}

    try:
        sel = Selector(text=str(url_opened.read()), type='html')
        repo = sel.xpath('/html/body/div[1]/div[2]/main/div/div[3]'
                         '/div/div[3]/a', type='html').get()

        if repo.find('github.com') != -1:
            libraries = {}
            libraries = json.loads(git_library(repo[repo.find(
                'href="') + 6:repo.find('" title=')], libraries))
            libraries[library] = libraries.pop(repo[repo.find('github.com')
                                                    + 11:repo.find('" title')])

        else:
            try:
                sel = Selector(text=str(urllib.request.urlopen(
                    url + '?tab=versions').read()), type='html')
                versions = []
                t = 2
                while t != 0:
                    ver = sel.xpath(f'/html/body/div[1]/div[2]/main/div/div/'
                                    f'div[2]/div[{t}]/a', type='html').get()
                    if ver is not None:
                        versions.append(
                            ver[ver.find('">') + 2:ver.find('</a>')])
                        t += 4
                    else:
                        t = 0

            except:
                libraries.clear()
                libraries['error'] = 'error'
                return json.dumps(libraries)

            try:
                for version in versions:
                    sel = Selector(text=str(urllib.request.urlopen(
                        url + '@' + version + '#section-sourcefiles')
                                            .read()), type='html')
                    down = sel.xpath('/html/body/div[2]/div/div/div[2]/div[2]'
                                     '/div[2]/ul/li[1]/a', type='html').get()

                    if down is not None:
                        libraries[library][version] = [
                            down[down.find('href=') + 6:
                                 down.find('" target=')], '']
                    else:
                        repo = sel.xpath('/html/body/div[2]/div/div/div[2]'
                                         '/div[2]/div[2]/ul/li[1]/a',
                                         type='html').get()
                        libraries[library][version] = [
                            repo[repo.find('href=') + 6:
                                 repo.find('" title=')], '']

            except:
                libraries.clear()
                libraries['error'] = 'error'
                return json.dumps(libraries)

    except requests.HTTPError as err:
        if err.response == 403:
            libraries.clear()
            libraries['error'] = 'error'
            print('Rate limit exceeded')
            return json.dumps(libraries)
    except Exception as e:
        libraries.clear()
        libraries['error'] = 'error'
        return json.dumps(libraries)

    return json.dumps(libraries)

# %%%%%%%%%% The End %%%%%%%%%%#
