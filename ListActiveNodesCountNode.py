import json
import warnings
import requests
from requests.packages.urllib3 import exceptions

endpoint = {}
endpoint['login'] = "admin"
endpoint['passwd'] = "P@ssw0rd"
method = "ListActiveNodes"
params = {}

url = 'https://solidfire.mvip/json-rpc/10.1'
payload = {'method': method, 'params': params}

with warnings.catch_warnings():
    warnings.simplefilter("ignore", exceptions.InsecureRequestWarning)
    req = requests.post(url,
                        data=json.dumps(payload),
                        auth=(endpoint['login'], endpoint['passwd']),
                        verify=False,
                        timeout=30)
    response = req.json()
    req.close()
    if 'error' in response:
        msg = ('API response: %s') % response
        raise Exception(msg)

node_count = len(response['result']['nodes'])
response['result'].update({"nodeCount":node_count})

dump_response = json.dumps(response)
print dump_response
