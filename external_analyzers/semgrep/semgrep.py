#!/usr/bin/env python3

# Detect Dangerous Functions in GO Packages
# -*- coding: utf-8 -*-

# %%%%%%%%%%% Libraries %%%%%%%%%%%#

import os
import errno
import json
import shutil
import subprocess
from json import JSONDecodeError
from auxiliar_functions.globals import tmp, semgrep_results


def semgrep_process(files):
    files.extractall(semgrep_results)
    package_name = files.filename.split('/')[-1]
    try:
        subprocess.run(["semgrep",
                        "--disable-version-check",
                        "--strict",
                        "--optimizations",
                        "all",
                        "--config",
                        "p/gosec",
                        semgrep_results + os.sep + files.namelist()[0],
                        "--json",
                        "-o",
                        semgrep_results + os.sep + package_name + '.json'
                        ],
                       stdout=subprocess.PIPE, shell=False, check=False)
        shutil.rmtree(f"{semgrep_results}{os.sep}{files.namelist()[0]}",
                      ignore_errors=True)
    except OSError as e:
        if e.errno == errno.ENOENT:
            raise OSError('SemGrep not installed')
    except:
        return json.dumps(['Called SemGrep Process Error'])

    try:
        with open(semgrep_results + os.sep + package_name + '.json', 'r') as f:
            json_data = json.load(f)

        return json_data

    except (FileNotFoundError, JSONDecodeError):
        return json.dumps(['Called Process Error'])