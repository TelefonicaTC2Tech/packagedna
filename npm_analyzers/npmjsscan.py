#!/usr/bin/env python3

# Finding Bugs with NJSScan Module
# -*- coding: utf-8 -*-

import json
import errno
import subprocess
from json import JSONDecodeError
from auxiliar_functions.globals import tmp


def npm_njsscan(files):
    files.extractall(tmp)

    try:
        subprocess.run(["njsscan",
                        "" + tmp + "",
                        "--json",
                        "-o",
                        tmp + "/report_njsscan"
                        ],
                       stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT,
                       shell=False, check=False)
    except OSError as e:
        if e.errno == errno.ENOENT:
            raise OSError('Njsscan not installed')
    except:
        return json.dumps(['Called Process Error'])

    try:
        with open(tmp + '/report_njsscan', 'r') as f:
            json_data = json.load(f)

        return json_data

    except (FileNotFoundError, JSONDecodeError):
        return json.dumps(['Called Process Error'])


# %%%%%%%%%% The End %%%%%%%%%%#
