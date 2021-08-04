
import os
import json
import shutil
from glob import glob
from auxiliar_functions.globals import sandbox
from auxiliar_functions.globals import url_vt_scan
from auxiliar_functions.globals import url_vt_report
from external_analyzers.virustotal.send_request_virustotal import \
    send_request_virustotal
from external_analyzers.virustotal.get_request_response_virustotal \
    import get_request_response_virustotal


def virustotal_analysis(path_package_name, virustotal_api_key):
    path_package_name = path_package_name.split('/')[-1].split('-')[0]
    sandbox_package_dir = sandbox + os.sep + path_package_name + '*' + '/**'
    onlyfiles = [f for f in glob(sandbox_package_dir, recursive=True)
                 if os.path.isfile(os.path.join(sandbox_package_dir, f))]

    all_virustotal_responses = []
    for file_path in onlyfiles:
        try:
            result_submit = {}
            result_analyze = {}
            validate_virustotal_restriction(file_path, virustotal_api_key)

            result_submit = send_request_virustotal(
                virustotal_api_key, url_vt_scan, file_path)
            result_analyze = get_request_response_virustotal(
                virustotal_api_key, url_vt_report, result_submit["resource"])
            prune_response = prune_virustotal_response(
                result_analyze, file_path)
            if prune_response:
                all_virustotal_responses.extend(prune_response)
        except ValueError:
            pass
        except ConnectionRefusedError:
            break
        except Exception:
            pass

    try:
        shutil.rmtree(sandbox)
    except:
        pass
    all_virustotal_responses = json.dumps(all_virustotal_responses)
    return all_virustotal_responses


def prune_virustotal_response(result_analyze, file_path):
    try:
        total = result_analyze['total']
        positives = result_analyze['positives']
        permalink = result_analyze['permalink']

        response = []
        if positives > 0:
            response.append(file_path)
            response.append(total)
            response.append(positives)
            response.append(permalink)
            return response
        return None
    except:
        return None


def validate_virustotal_restriction(path_package_name, virustotal_api_key):
    file_size = os.path.getsize(path_package_name)

    if file_size > 30_000_000:
        raise ValueError('VirusTotal Restriction: File size too large...')
    if not virustotal_api_key:
        print("No VirusTotal API key...!")
        return json.dumps('[]')
