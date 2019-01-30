import json
import requests

headers = {'Content-Type': 'application/json'}

def get_member_info(uid):
    body = {'username': 'makerspace_api', 'password': 'makerspace_password'}

    r = requests.post('http://ADDRESS/auth', data = json.dumps(body), headers=headers)

    access_token = r.json()['access_token']

    auth_headers = {'Authorization': 'JWT ' + access_token}

    r = requests.get('http://ADDRESS/user', headers=auth_headers, params={'uid': uid})

    return r.json()
