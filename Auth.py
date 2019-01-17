import json
import requests

headers = {'Content-Type': 'application/json'}

def get_member_info(uid):
    body = {'username': 'makerapi', 'password': '***REMOVED***'}

    r = requests.post('http://***REMOVED***/auth', data = json.dumps(body), headers=headers)

    access_token = r.json()['access_token']

    auth_headers = {'Authorization': 'JWT ' + access_token}

    r = requests.get('http://***REMOVED***/user', headers=auth_headers, params={'uid': uid})

    return r.json()
