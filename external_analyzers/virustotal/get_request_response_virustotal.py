
import json
import requests
from time import sleep

BAR = [
    " [=     ]",
    " [ =    ]",
    " [  =   ]",
    " [   =  ]",
    " [    = ]",
    " [     =]",
    " [    = ]",
    " [   =  ]",
    " [  =   ]",
    " [ =    ]",
]


def get_request_response_virustotal(API_KEY_VT, URL_VT_REPORT, resource_id):
    try:
        response = {}
        headers = {"User-Agent": "Mozilla/5.0 (X11; Linux i686; rv:64.0)"
                                 " Gecko/20100101 Firefox/64.0"}
        post_data = {'apikey': API_KEY_VT,
                     'resource': resource_id}
        response = requests.get(URL_VT_REPORT,
                                params=post_data,
                                headers=headers)
        if response.status_code == 204:
            raise ConnectionRefusedError("VirusTotal request rate "
                                         "limit exceeded.")
        if not response.status_code == 200:
            raise Exception('VirusTotal error!')
        else:
            response = json.loads(response.content)
            i = 0
            while response['response_code'] != 1:
                print(f' Waiting for VirusTotal response{BAR[i % len(BAR)]}',
                      end="\r")
                sleep(0.5)
                i += 1
                if i % 40 == 0:
                    try:
                        response = requests.get(URL_VT_REPORT,
                                                params=post_data,
                                                headers=headers).json()
                    except Exception:
                        raise Exception('VirusTotal error!')
        return response

    except Exception as e:
        print("exception " + str(e))
        return None
