import gc
import os
import sys
import json
import shutil

from time import sleep
from pathlib import Path
from colorama import reinit
from colorama import Fore
from colorama import Style

from auxiliar_functions.banner import banner
from auxiliar_functions.messages import wrongs
from auxiliar_functions.globals import configurations_path
from auxiliar_functions.globals import (
    tmp,
    flask_server_data_folder,
    url_py,
    url_rb,
    url_go,
    url_npm,
    sandbox,
    downloads,
    go_pkgs,
    npm_pkgs,
    pypi_pkgs,
    ruby_pkgs,
    appinspector_results
)


def create_dir():
    dir_to_create = [downloads,
                     pypi_pkgs,
                     ruby_pkgs,
                     npm_pkgs,
                     go_pkgs,
                     sandbox,
                     tmp,
                     flask_server_data_folder,
                     flask_server_data_folder + os.sep + 'python',
                     flask_server_data_folder + os.sep + 'ruby',
                     flask_server_data_folder + os.sep + 'npm',
                     flask_server_data_folder + os.sep + 'go',
                     appinspector_results
                     ]
    dir_to_delete = [sandbox,
                     tmp
                     ]
    [shutil.rmtree(dir_path, ignore_errors=True) for dir_path in dir_to_delete]
    sleep(.1)
    [os.makedirs(dir_path, exist_ok=True) for dir_path in dir_to_create]


def input_pack(lang='', package_name=None,
               message="[!] Digit name of Package: "):
    if not package_name:
        package_name = input(Fore.CYAN + Style.NORMAL + message
                             + Style.RESET_ALL)
    os.system('cls' if os.name == 'nt' else 'clear')
    libraries = {}
    if lang == 'py':
        package_name = package_name.strip().replace('_', '-')
        url = url_py + package_name
    elif lang == 'rb':
        url = url_rb + '/' + package_name
    elif lang == 'npm':
        url = url_npm + package_name
    elif lang == 'go':
        url = url_go + package_name
    else:
        file_path = Path(package_name)
        if not file_path.is_file():
            raise ValueError('Invalid Path')
        url = ''

    return [package_name, url, libraries]


def input_code_extract(message=''):
    package_name = input(Fore.CYAN + Style.NORMAL + message + Style.RESET_ALL)
    return package_name


def end_execution():
    wrongs(6)
    sys.exit(0)


def clear_terminal():
    gc.collect()
    sleep(.1)
    os.system('cls' if os.name == 'nt' else 'clear')
    reinit()
    banner()


def selection_wrong():
    wrongs(1)
    sleep(.5)
    gc.collect()
    clear_terminal()


def not_implemented_yet():
    wrongs(10)
    sleep(.5)
    gc.collect()
    clear_terminal()


def get_app_inspector_path():
    try:
        with open(configurations_path, "r") as read_file:
            data = json.load(read_file)
            appinspector_path = Path(data['appinspector_path'])
        return appinspector_path
    except:
        pass


def get_virus_total_api_key():
    try:
        with open(configurations_path, "r") as read_file:
            data = json.load(read_file)
        return data['virustotal_key']
    except:
        pass


def get_libraries_io_api_key():
    try:
        with open(configurations_path, "r") as read_file:
            data = json.load(read_file)
        return data['libraries_io']
    except:
        pass


def get_bitbucket_auth():
    try:
        with open(configurations_path, "r") as read_file:
            data = json.load(read_file)
        return data['bitbucket']
    except:
        pass


def get_github_api_token():
    try:
        with open(configurations_path, "r") as read_file:
            data = json.load(read_file)
        return data['github_token']
    except:
        pass