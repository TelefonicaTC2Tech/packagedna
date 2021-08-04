import json

from colorama import Fore, Style
from auxiliar_functions.messages import wrongs
from auxiliar_functions.messages import tittles
from auxiliar_functions.globals import SEPARATOR
from auxiliar_functions.messages import subtittles


def print_cves_json(cves_json, package_input_name):
    tittles(7, package_input_name)

    for json_pack in cves_json:
        cves_dict = json.loads(json_pack)
        for key in cves_dict:
            try:
                print(f"[*] CVE: {key}")
                for key2 in cves_dict[key]:
                    print(f"[*] Description: {cves_dict[key][key2].get('name', '')}")
                    print(f"[*] Date: {cves_dict[key][key2].get('date', '')}")
                    print(f"[*] Severity: {cves_dict[key][key2].get('severity', '')}")
                    print(f"[*] Affected: {cves_dict[key][key2].get('affected', '')}")
                    print(f"[*] Url: {cves_dict[key][key2].get('url', '')}")
                print("[*]\n")
            except TypeError:
                pass


def print_metadata_json(metadata_json, package_input_name):
    tittles(3, package_input_name)
    for json_pack in metadata_json:
        try:
            metadata_dict = json.loads(json_pack)
            print(f"[*]\t Name: {metadata_dict['name']}")
            print(f"[*]\t Author: {metadata_dict['author']}")
            print(f"[*]\t Author Email: {metadata_dict['author_email']}")
            print(f"[*]\t Version: {metadata_dict['version']}")
            print(f"[*]\t Date: {metadata_dict['date']}")
            print(f"[*]\t License: {metadata_dict['license']}")
            print(f"[*]\t Home Page: {metadata_dict['home_page']}")
            print(f"[*]\n")
        except:
            pass


def print_dangerous_functions_json(dangerous_functions_json,
                                   package_input_name):
    tittles(6, package_input_name)
    for json_pack in dangerous_functions_json:
        dangerous_functions_dict = json.loads(json_pack)
        for key in dangerous_functions_dict:
            if key == 'file':
                subtittles(5, dangerous_functions_dict[key])
            elif key == 'dangerous_functions':
                for value in dangerous_functions_dict[key]:
                    print(value)
        print(f"[*]\n")


def print_hashfiles_json(hashfiles_json, package_input_name):
    tittles(4, package_input_name)
    for json_pack in hashfiles_json:
        try:
            hashfiles_dict = json.loads(json_pack)
            for key in hashfiles_dict.keys():
                if key != 'pkg_hashid':
                    print(f"[*] SHA256 - {key}: {hashfiles_dict[key]}")
        except:
            pass


def print_extract_data_json(extract_data_json, package_input_name):
    tittles(5, package_input_name)
    for json_pack in extract_data_json:
        try:
            extract_data_dict = json.loads(json_pack)
        except:
            pass
        try:
            if len(extract_data_dict['urls']) > 0:
                subtittles(1, extract_data_dict['name'])
                for url in extract_data_dict['urls']:
                    print('[*]\t' + url)
                print(f"[*]\n")
        except (KeyError, TypeError):
            pass

        try:
            if len(extract_data_dict['hashs']) > 0:
                subtittles(2, extract_data_dict['name'])
                for hash in extract_data_dict['hashs']:
                    print('[*]\t' + hash)
                print(f"[*]\n")
        except (KeyError, TypeError):
            pass

        try:
            if len(extract_data_dict['ips']) > 0:
                subtittles(3, extract_data_dict['name'])
                for ip in extract_data_dict['ips']:
                    print('[*]\t' + ip)
                print(f"[*]\n")
        except (KeyError, TypeError):
            pass

        try:
            if len(extract_data_dict['emails']) > 0:
                subtittles(4, extract_data_dict['name'])
                for email in extract_data_dict['emails']:
                    print('[*]\t' + email)
                print(f"[*]\n")
        except (KeyError, TypeError):
            pass


def print_appinspector_json(appinspector_json, package_input_name):

    if any('Called Process Error' in x for x in appinspector_json):
        wrongs(9, package_input_name)
        print('[*]\tAppInspector execution failed.')
        print('[*]\tPlease, install this dependency from: '
              'https://github.com/microsoft/ApplicationInspector')
        print('[*]\n')
    else:
        tittles(8, package_input_name)
        for json_pack in appinspector_json:
            appinspector_dict = json.loads(json_pack)
            for match_list in appinspector_dict:
                print(f'[*]\tRule name: {match_list["rule_name"]}')
                print(f'[*]\tConfidence: {match_list["confidence"]}')
                print(f'[*]\tSeverity: {match_list["severity"]}')
                print(f'[*]\tFilename: {match_list["filename"]}')
                print(f'[*]\tsample: {match_list["sample"]}')
                print(f'[*]\tStart line: {match_list["start_line"]}')
                print(f'[*]\tEnd line: {match_list["end_line"]}')
                exceprt = match_list["excerpt"].replace(
                    "&#39;", "'").replace('&quot;', '"')
                print(f'[*]\tExceprt: \n\n{exceprt}')
                print(f"[*]\n")


def print_user_dev_json(user_dev_json, package_input_name):
    tittles(11, package_input_name)
    for dev_json in user_dev_json:
        try:
            dict_devs = json.loads(dev_json)
            for i in dict_devs:
                print(Fore.GREEN + Style.BRIGHT +
                      f"[*]\t\tUsername: {dict_devs[i]['username']}")
                print(
                    Fore.GREEN + Style.BRIGHT + f"[*]\t\tName: "
                                                f"{dict_devs[i]['name']}")
                print(Fore.GREEN + Style.BRIGHT + f"[*]\t\tRepositories:")
                for repo in dict_devs[i]['yours_repositories']:
                    print(Fore.GREEN + Style.BRIGHT +
                          f"[*]\t\t\tLanguage: "
                          f"{dict_devs[i]['yours_repositories'][repo]['language']}")
                    print(Fore.GREEN + Style.BRIGHT +
                          f"[*]\t\t\t\tUrl: "
                          f"{dict_devs[i]['yours_repositories'][repo]['url']}")
                    print(f"[*]\n")


        except:
            print(Fore.RED + Style.BRIGHT + f"[*]\t\tNo data found.")


def print_library(libraries):
    if not isinstance(libraries, str):
        for pack in libraries.keys():
            tittles(2, pack)
            for ver in libraries[pack].keys():
                print('[*]')
                print('[*]\t' + ver + ":")
                print('[*]\t\tURL   : ' + libraries[pack][ver][0])
                print('[*]\t\tSHA256: ' + libraries[pack][ver][1][0:64])


def print_typosquatting(typosquatting_json, package_input_name):
    tittles(9, package_input_name)
    typosquatting_dict = json.loads(typosquatting_json)
    if typosquatting_dict:
        for key in typosquatting_dict:
            print(f'[*]\tPackage name: {key}')
            print(f'[*]\tURL: {typosquatting_dict[key]}')
            print(f"[*]\n")
    else:
        print(f"[*]\tNo typosquatting found")
        print(f"[*]\n")


def print_appinspector_path_error():
    print('\n')
    print(Fore.RED + Style.BRIGHT + SEPARATOR)
    print(Fore.RED + Style.BRIGHT + '[*] AppInspector path is missing.'
                                    ' This analysis will not be executed.')
    print(Fore.RED + Style.BRIGHT + SEPARATOR)


def print_virustotal_api_key_error():
    print('\n')
    print(Fore.RED + Style.BRIGHT + SEPARATOR)
    print(Fore.RED + Style.BRIGHT + '[*] VirusTotal API Key is missing.'
                                    ' This analysis will not be executed.')
    print(Fore.RED + Style.BRIGHT + SEPARATOR)


def print_njsscan_not_installed_error():
    print('\n')
    print(Fore.RED + Style.BRIGHT + SEPARATOR)
    print(Fore.RED + Style.BRIGHT + '[*] Njsscan is not installed.'
                                    ' This analysis will not be executed.')
    print(Fore.RED + Style.BRIGHT + SEPARATOR)


def print_njsscan_not_installed_error():
    print('\n')
    print(Fore.RED + Style.BRIGHT + SEPARATOR)
    print(Fore.RED + Style.BRIGHT + '[*] Njsscan is not installed.'
                                    ' This analysis will not be executed.')
    print(Fore.RED + Style.BRIGHT + SEPARATOR)


def print_semgrep_not_installed_error():
    print('\n')
    print(Fore.RED + Style.BRIGHT + SEPARATOR)
    print(Fore.RED + Style.BRIGHT + '[*] SempGrep is not installed.'
                                    ' This analysis will not be executed.')
    print(Fore.RED + Style.BRIGHT + SEPARATOR)


def print_rubocop_not_installed_error():
    print('\n')
    print(Fore.RED + Style.BRIGHT + SEPARATOR)
    print(Fore.RED + Style.BRIGHT + '[*] Rubocop is not installed.'
                                    ' This analysis will not be executed.')
    print(Fore.RED + Style.BRIGHT + SEPARATOR)


def print_bandit_not_installed_error():
    print('\n')
    print(Fore.RED + Style.BRIGHT + SEPARATOR)
    print(Fore.RED + Style.BRIGHT + '[*] Bandit is not installed.'
                                    ' This analysis will not be executed.')
    print(Fore.RED + Style.BRIGHT + SEPARATOR)


def print_username(json_user, source):
    try:
        dict_user = json.loads(json_user)
    except:
        dict_user = ''
    print('\n')
    print(Fore.GREEN + Style.BRIGHT + SEPARATOR)
    print(Fore.GREEN + Style.BRIGHT + f"[*] {source}")
    try:
        print(Fore.GREEN + Style.BRIGHT + f"[*]\t\tUsername: "
                                          f"{dict_user['username']}")
        print(Fore.GREEN + Style.BRIGHT + f"[*]\t\tName: {dict_user['name']}")
        print(Fore.GREEN + Style.BRIGHT + f"[*]\t\tRepositories:")
        for repo in dict_user['yours_repositories']:
            print(Fore.GREEN + Style.BRIGHT +
                  f"[*]\t\t\tLanguage: "
                  f"{dict_user['yours_repositories'][repo]['language']}")
            print(Fore.GREEN + Style.BRIGHT +
                  f"[*]\t\t\t\tUrl: "
                  f"{dict_user['yours_repositories'][repo]['url']}")
    except:
        print(Fore.RED + Style.BRIGHT + f"[*]\t\tNo data found.")
    print(Fore.GREEN + Style.BRIGHT + SEPARATOR)
