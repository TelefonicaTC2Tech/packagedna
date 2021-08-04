#!/usr/bin/env python3

# Finding Bugs with Rubocop Module
# -*- coding: utf-8 -*-

import json
import errno
import tarfile
import shutil
import subprocess
from json import JSONDecodeError
from auxiliar_functions.globals import tmp


def rb_rubocop(files):
    files.extractall(tmp)

    file_data = tarfile.open(tmp+'/data.tar.gz', 'r:gz')
    file_data.extractall(tmp)

    try:
        subprocess.run(["rubocop",
                        "" + tmp + "",
                        "--force-default-config",
                        "--cache",
                        "false",
                        "-f",
                        "json",
                        "-o",
                        tmp + "/report_rubocop"],
                       stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT,
                       shell=False, check=False)
    except OSError as e:
        if e.errno == errno.ENOENT:
            raise OSError('Rubocop not installed')
    except:
        return json.dumps(['Called Process Error'])

    try:
        with open(tmp + '/report_rubocop', 'r') as f:
            json_data = json.load(f)
            list_critical_matches = []

            for row in json_data['files']:
                for row_offenses in row['offenses']:
                    if row_offenses['severity'] in ['warning',
                                                    'error', 'fatal']:
                        dict_critical_matches = {
                            'filename': row['path'],
                            'severity': row_offenses['severity'],
                            'message': row_offenses['message'],
                            'cop_name': row_offenses['cop_name'],
                            'start_line': row_offenses[
                                'location']['start_line'],
                            'end_line': row_offenses['location']['last_line']
                        }
                        list_critical_matches.append(dict_critical_matches)
    except (FileNotFoundError, JSONDecodeError):
        return json.dumps(['Called Process Error'])

    shutil.rmtree(tmp, ignore_errors=True)
    try:
        list_critical_matches = json.dumps(list_critical_matches)
    except UnboundLocalError:
        list_critical_matches = json.dumps([''])
    return list_critical_matches

# %%%%%%%%%% The End %%%%%%%%%%#
