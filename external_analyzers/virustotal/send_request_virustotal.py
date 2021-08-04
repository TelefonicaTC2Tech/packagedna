
import json
import requests
from time import sleep
from multiprocessing.pool import ThreadPool

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


def send_request_virustotal(API_KEY_VT, URL_VT_SCAN, filepath):
    try:
        response = {}
        headers = {"User-Agent": "Mozilla/5.0 (X11; Linux i686;"
                                 " rv:64.0) Gecko/20100101 Firefox/64.0"}
        post_data = {'apikey': API_KEY_VT}
        files = {'file': (filepath, open(filepath, 'rb'))}
        pool = ThreadPool(processes=1)
        async_result = pool.apply_async(requests.post,
                                        kwds={'url': URL_VT_SCAN,
                                              'files': files,
                                              'params': post_data,
                                              'headers': headers})

        i = 0
        while not async_result.ready():
            print(f' Uploading file to VirusTotal {BAR[i % len(BAR)]}',
                  end="\r")
            sleep(0.5)
            i += 1

        response = async_result.get()
        if not response.status_code == 200:
            raise Exception('VirusTotal error!')
        else:
            response = json.loads(response.content)

        return response
    except Exception as e:
        raise Exception('VirusTotal error!')
