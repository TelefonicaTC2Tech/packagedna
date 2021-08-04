
import json
import urllib3
from bitbucket.client import Client
from auxiliar_functions.auxiliar_functions import get_bitbucket_auth

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def user_bitbucker(username):
    user_bb = {}
    auth = get_bitbucket_auth()
    try:
        bb = Client(auth[0], auth[1], username)
        data = bb.get_repositories()
        if len(data['values']) > 0:
            user_bb['username'] = data['values'][0]['owner']['nickname']
            user_bb['name'] = data['values'][0]['owner']['display_name']
            user_bb['yours_repositories'] = {}
            i = 0

            while i < len(data['values']):
                name_repo = data['values'][i]['name']
                user_bb['yours_repositories'][name_repo] = dict(
                    language=data['values'][i]['language'],
                    url=data['values'][i]['links']['html']['href'])
    except:
        user_bb = {'name': username, 'status': 'error bitbucket'}

    return json.dumps(user_bb, ensure_ascii=False)






