
import os
import json
import subprocess
import logging
import datetime


def generate_json(cve_json=None,
                  metadata_json=None,
                  dangerous_function_json=None,
                  analysis_bandit_json=None,
                  analysis_rubocop_json=None,
                  analysis_njsscan_json=None,
                  analysis_go_semgrep_json=None,
                  hash_files_json=None,
                  extract_data_json=None,
                  app_inspector_json=None,
                  typo_json=None,
                  virus_total_json=None,
                  user_dev_json=None,
                  extra_json=None):
    flag = False

    json_to_html = {}
    try:
        cve_dict = {}
        [cve_dict.update(json.loads(cve)) for cve in list(cve_json)]
    except:
        cve_dict = []
    for idx, row in enumerate(metadata_json):
        metadata_dict = json.loads(metadata_json[idx])
        try:
            dangerous_function_dict = json.loads(dangerous_function_json[idx])
        except IndexError:
            dangerous_function_dict = ''
        try:
            analysis_bandit_dict = analysis_bandit_json[idx]
        except IndexError:
            analysis_bandit_dict = ''
        try:
            analysis_rubocop_dict = json.loads(analysis_rubocop_json[idx])
        except (IndexError, json.JSONDecodeError, TypeError):
            analysis_rubocop_dict = ''
        try:
            analysis_njsscan_dict = analysis_njsscan_json[idx]
        except IndexError:
            analysis_njsscan_dict = ''
        try:
            analysis_go_semgrep_dict = analysis_go_semgrep_json[idx]
        except IndexError:
            analysis_go_semgrep_dict = ''
        try:
            virus_total_dict = json.loads(virus_total_json[idx])
        except (IndexError, TypeError):
            virus_total_dict = ''
        try:
            app_inspector_dict = json.loads(app_inspector_json[idx])
        except IndexError:
            app_inspector_dict = ''
        try:
            extra_dict = json.loads(extra_json)
        except IndexError:
            extra_dict = ''

        try:
            user_dev_dict = json.loads(user_dev_json[idx])
        except:
            user_dev_json = ''
        hash_files_dict = json.loads(hash_files_json[idx])
        extract_data_dict = json.loads(extract_data_json[idx])
        try:
            typo_dict = json.loads(typo_json)
        except:
            typo_dict = []

        """ Estadisticas del reporte """

        totals_rubocop = dict(Critical=0, Warning=0, Error=0, other=0)
        totals_njsscan = dict(Warning=0, Error=0, other=0)
        totals_bandit = dict(Confidencial=dict(High=0, Medium=0),
                             Severity=dict(High=0, Medium=0))
        totals_appinspector = dict(Confidencial=
                                   dict(Critical=0, High=0, Medium=0),
                                   Severity=dict(Critical=0, High=0, Medium=0))

        try:
            if type(analysis_rubocop_dict) is list:
                for item in analysis_rubocop_dict:
                    if item['severity'] == 'critical':
                        totals_rubocop['Critical'] += 1
                    elif item['severity'] == 'warning':
                        totals_rubocop['Warning'] += 1
                    elif item['severity'] == 'error':
                        totals_rubocop['Error'] += 1
                    else:
                        totals_rubocop['other'] += 1
            if (type(analysis_bandit_dict) is dict) and \
                    ('results' in analysis_bandit_dict):
                for item in analysis_bandit_dict['results']:
                    if item['issue_confidence'] == 'HIGH':
                        totals_bandit['Confidencial']['High'] += 1
                    elif item['issue_confidence'] == 'MEDIUM':
                        totals_bandit['Confidencial']['Medium'] += 1
                    if item['issue_severity'] == 'HIGH':
                        totals_bandit['Severity']['High'] += 1
                    elif item['issue_severity'] == 'MEDIUM':
                        totals_bandit['Severity']['Medium'] += 1
            if type(app_inspector_dict) is list:
                for item in app_inspector_dict:
                    if item['confidence'] == 'High':
                        totals_appinspector['Confidencial']['High'] += 1
                    elif item['confidence'] == 'Medium':
                        totals_appinspector['Confidencial']['Medium'] += 1
                    elif item['confidence'] == 'Critical':
                        totals_appinspector['Confidencial']['Critical'] += 1
                    if item['severity'] == 'High':
                        totals_appinspector['Severity']['High'] += 1
                    elif item['severity'] == 'Medium':
                        totals_appinspector['Severity']['Medium'] += 1
                    elif item['severity'] == 'Critical':
                        totals_appinspector['Severity']['Critical'] += 1
            if (type(analysis_njsscan_dict) is dict) and\
                    ('nodejs' in analysis_njsscan_dict):
                for item in analysis_njsscan_dict['nodejs']:
                    if analysis_njsscan_dict['nodejs'][item]['metadata'][
                            'severity'] == 'WARNING':
                        totals_njsscan['Warning'] += 1
                    elif analysis_njsscan_dict['nodejs'][item]['metadata'][
                            'severity'] == 'ERROR':
                        totals_njsscan['Error'] += 1
                    else:
                        totals_njsscan['other'] += 1


            if type(dangerous_function_dict) is dict:
                totals_dangerous = len(dangerous_function_dict[
                                           'dangerous_functions'])
            else:
                totals_dangerous = 0
            if type(cve_dict) is dict:
                totals_cve = len(cve_dict.keys())
            else:
                totals_cve = 0
        except:
            pass

        try:
            if extra_dict == 'python':
                publish_date = datetime.datetime.strptime(
                    metadata_dict['date'], "%Y-%m-%dT%H:%M:%S").strftime(
                    '%Y-%m-%d %H:%M:%S')
            else:
                publish_date = metadata_dict['date']

            package_name = metadata_dict['name'].replace('/', '_-_').lower()
            json_to_html[f'{metadata_dict["version"]}'] = {
                'name': metadata_dict['name'],
                'version': metadata_dict['version'],
                'author': metadata_dict['author'],
                'date': publish_date,
                'license': metadata_dict['license'],
                'author_email': metadata_dict['author_email'],
                'home_page': metadata_dict['home_page'],
                'dangerous_function': dangerous_function_dict if
                'dangerous_functions' in dangerous_function_dict else '',
                'hash_files': {
                    key: hash_files_dict[key]
                    for key in hash_files_dict
                    }}
        except:
            package_name = 'package_name_not_found'
            continue
        try:
            json_to_html[f'{metadata_dict["version"]}']['data_collected'] = {
                'urls': [
                    url
                    for url in extract_data_dict['urls']
                    ],
                'hashs': [
                    hashes if 'hashs' in extract_data_dict else ''
                    for hashes in extract_data_dict['hashs']
                    ],
                'ips': [
                    ip if 'ips' in extract_data_dict else ''
                    for ip in extract_data_dict['ips']
                    ],
                'emails': [
                    email if 'emails' in extract_data_dict else ''
                    for email in extract_data_dict['emails']
                    ]
            }
        except (TypeError, KeyError):
            json_to_html[f'{metadata_dict["version"]}']['data_collected'] = {
                'urls': '',
                'hashs': '',
                'ips': '',
                'emails': ''
            }
            

        try:
            json_to_html[f'{metadata_dict["version"]}']['appinspector'] = {
                idx: x
                for idx, x in enumerate(app_inspector_dict)
            }
            flag = True
        except KeyError:
            json_to_html[f'{metadata_dict["version"]}']['appinspector'] = ''

        try:
            json_to_html[f'{metadata_dict["version"]}']['bandit'] = {   
                'errors': {
                    idx: x
                    for idx, x in enumerate(analysis_bandit_dict['errors']) 
                },
                'generated_at': analysis_bandit_dict['generated_at'] 
                ,
                'metrics': analysis_bandit_dict['metrics'] 
                ,
                'results': {
                    idx: x
                    for idx, x in enumerate(analysis_bandit_dict['results']) 
                }
            }
            flag = True
        except (KeyError, TypeError):
            json_to_html[f'{metadata_dict["version"]}']['bandit'] = ''

        try:
            json_to_html[f'{metadata_dict["version"]}']['rubocop'] = {
                idx: x
                for idx, x in enumerate(analysis_rubocop_dict)
            }
            flag = True
        except KeyError:
            json_to_html[f'{metadata_dict["version"]}']['rubocop'] = ''

        try:
            json_to_html[f'{metadata_dict["version"]}']['njsscan'] = {
                'errors': {
                    idx: x
                    for idx, x in enumerate(analysis_njsscan_dict['errors'])
                },
                'nodejs': analysis_njsscan_dict['nodejs']
                ,
                'templates': {
                    idx: x
                    for idx, x in enumerate(analysis_njsscan_dict['templates'])
                }
            }
            flag = True
        except (KeyError, TypeError):
            json_to_html[f'{metadata_dict["version"]}']['njsscan'] = ''

        try:
            json_to_html[f'{metadata_dict["version"]}']['goscan'] = {
                'results': {
                    idx: x
                    for idx, x in enumerate(analysis_go_semgrep_dict['results'])
                },
                'errors': {
                    idx: x
                    for idx, x in enumerate(analysis_go_semgrep_dict['errors'])
                }
            }
            flag = True
        except (KeyError, TypeError):
            json_to_html[f'{metadata_dict["version"]}']['goscan'] = ''

        try:
            json_to_html[f'{metadata_dict["version"]}']['typo_urls'] = {
                name: typo_dict[name]
                for name in typo_dict
            }
        except KeyError:
            json_to_html[f'{metadata_dict["version"]}']['typo_urls'] = ''

        try:
            json_to_html[f'{metadata_dict["version"]}']['virustotal'] = {
                'file_path': virus_total_dict[0],
                'total_engines': virus_total_dict[1],
                'positive_engines': virus_total_dict[2],
                'permalink': virus_total_dict[3]
            }
            flag = True
        except IndexError:
            json_to_html[f'{metadata_dict["version"]}']['virustotal'] = ''

        try:
            cve_version_dict = cve_dict.get(metadata_dict['version'], None)
            if cve_version_dict:
                json_to_html[f'{metadata_dict["version"]}']['cves'] = {
                    key: {'cve': key,
                          'name': cve_version_dict[key]['name'],
                          'date': cve_version_dict[key]['date'],
                          'severity': cve_version_dict[key]['severity'],
                          'affected': cve_version_dict[key]['affected'],
                          'url': cve_version_dict[key]['url']
                          }
                    for key in cve_version_dict
                }
        except KeyError:
            pass

        try:
            json_to_html[f'{metadata_dict["version"]}']['extra'] = {
                'programming_language': extra_dict
            }
        except KeyError:
            pass
        try:
            json_to_html[f'{metadata_dict["version"]}']['users'] = {}
            for user_dict in user_dev_dict:
                user = user_dev_dict[user_dict]
                json_to_html[
                    f'{metadata_dict["version"]}']['users'][user['username']] \
                    = {'Username': user['username'], 'Name': user['name'],
                       'Repositories': {
                        key: {
                            'Language': user['yours_repositories'][key]
                            ['language'], 'Url': user['yours_repositories']
                            [key]['url']
                        }
                        for key in user['yours_repositories']
                    }
                }
        except KeyError:
            pass

    if flag:
        try:
            logging.warning(f'Package name: {package_name}')
        except:
            pass
    script_dir_path = f'{os.path.dirname(os.path.realpath(__file__))}' \
                      f'/static/data/{extra_dict}/'
    os.chdir(script_dir_path)
    with open(script_dir_path + package_name, 'w', encoding='utf-8') as f:
        json.dump(json_to_html, f, ensure_ascii=False, indent=4)
    os.environ['PACKAGE_LANGUAGE'] = extra_dict


def run_server(package_name):
    flask_path = os.path.dirname(os.path.realpath(__file__))
    os.environ['JSON_PACKAGE_NAME'] = package_name
    subprocess.call(['python3', flask_path + '/app.py'])
