#!/usr/bin/env python3

# Finding Bugs with Bandit Module
# -*- coding: utf-8 -*-

import json
import errno
import subprocess
from json import JSONDecodeError
from auxiliar_functions.globals import tmp


def py_analysis_bandit(files):
    files.extractall(tmp)

    try:
        subprocess.run(["bandit",
                        "-r",
                        "" + tmp + "",
                        "-f",
                        "json",
                        "-o",
                        tmp + "/bandit_report"],
                       stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT,
                       shell=False, check=False)
    except OSError as e:
        if e.errno == errno.ENOENT:
            raise OSError('Bandit not installed')
    except:
        return json.dumps(['Called Process Error'])

    try:
        with open(tmp + '/bandit_report', 'r') as f:
            json_data = json.load(f)
            return json_data

    except (FileNotFoundError, JSONDecodeError):
        return json.dumps(['Called Process Error'])

# %%%%%%%%%% The End %%%%%%%%%%#
