#!/usr/bin/env python3

# Detect Dangerous Functions in python packages
# -*- coding: utf-8 -*-

# %%%%%%%%%%% Libraries %%%%%%%%%%%#

import os
import json
import shutil
import subprocess
from auxiliar_functions.globals import tmp

# %%%%%%% Context Variables %%%%%%%#
# https://www.kevinlondon.com/2015/07/26/dangerous-python-functions.html
# https://datatheorem.github.io/python/2018/06/26/flake8-plugin/


# %%%%%%%%%%% Functions %%%%%%%%%%%#


def py_dangerous_functions(path_pack, files, pkg_hashid):
    files.extractall(tmp)

    os.chdir(tmp)
    data = subprocess.run(["flake8",
                           "--enable-extensions=B1 ",
                           # "--warn-symbols=$'obsolte_module=Warning!",
                           # "--ignore=E501, E251, E302, E305, E303,
                           # W503, E203"],  # TODO: Ver esto
                           "--select=E9,W6"],
                          # "\nmodule.obsolete_function=Warning!'"],
                          stdout=subprocess.PIPE, shell=False)
    try:
        fun = {}
        for line in data.stdout.decode('utf-8').split('\n'):
            if len(line.split(':')[0]) > 5:
                if fun.get(line.split(':')[0]) is None:
                    fun[line.split(':')[0]] = []
                    fun[line.split(':')[0]].append(line.split(':', 3)[1::])
                else:
                    fun[line.split(':')[0]].append(line.split(':', 3)[1::])
        data_issues = []
        for file in fun:
            for dang in fun[file]:
                line_col_issue = '[*] Ln: ' + dang[0] + ', Col: ' + dang[1]\
                                 + '  --  ' + dang[-1]
                data_issues.append(line_col_issue)
            file = file.replace(".", "-")
            dangerous_functions_found = {
                'pkg_hashid': pkg_hashid,
                'file': file,
                'dangerous_functions': data_issues
            }
    except:
        dangerous_functions_found = json.dumps([''])
    try:
        shutil.rmtree(tmp)
    except (FileNotFoundError, OSError):
        pass
    os.makedirs(tmp, exist_ok=True)

    try:
        dangerous_functions_found = json.dumps(dangerous_functions_found)
    except UnboundLocalError:
        dangerous_functions_found = json.dumps([''])
    return dangerous_functions_found

# %%%%%%%%%% The End %%%%%%%%%%#
