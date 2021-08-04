#!/usr/bin/env python3

# Detect Dangerous Functions in python packages
# -*- coding: utf-8 -*-

# %%%%%%%%%%% Libraries %%%%%%%%%%%#

import os
from pathlib import Path
import re
import json
import subprocess
from json import JSONDecodeError
from auxiliar_functions.globals import appinspector_results


def appinspector_process(path_pack, files, appinspector_path):
    name_pack = Path(path_pack).resolve().stem
    try:
        subprocess.run(["dotnet",
                        appinspector_path,
                        "analyze",
                        "-s",
                        path_pack,
                        "-f",
                        "json",
                        "-o",
                        appinspector_results + os.sep + name_pack + '.json'],
                       stdout=subprocess.PIPE, shell=False, check=False)
    except:
        return json.dumps(['Called Process Error'])

    try:
        with open(
                appinspector_results + os.sep + name_pack + '.json', 'r') as f:
            json_data = json.load(f)
            list_critical_matches = []
            if 'detailedMatchList' in json_data['metaData']:
                for row in json_data['metaData']['detailedMatchList']:
                    if re.search(".whl$", path_pack) or re.search(
                            ".tar.gz", path_pack) or \
                            re.search('tgz', path_pack) or \
                            re.search('.gem', path_pack) or \
                            'go_pkgs' in path_pack:
                        if (row.get('severity', "").lower() in ['critical',
                                                                'important']) \
                                or (row.get('pattern', "").lower() ==
                                    'base64'):
                            dict_critical_matches = {
                                'file_name': name_pack,
                                'rule_name': row['ruleName'],
                                'confidence': row['confidence'],
                                'severity': row['severity'],
                                'filename': row['fileName'],
                                'sample': row['sample'],
                                'start_line': row['startLocationLine'],
                                'end_line': row['endLocationLine'],
                                'excerpt': row['excerpt']
                            }
                            list_critical_matches.append(dict_critical_matches)
    except (FileNotFoundError, JSONDecodeError):
        return json.dumps(['Called Process Error'])

    list_critical_matches = json.dumps(list_critical_matches)
    return list_critical_matches
