import json
import warnings
import requests
from requests.packages.urllib3 import exceptions

endpoint = {}
endpoint['login'] = "admin"
endpoint['passwd'] = "P@ssw0rd"
method = "ListVolumes"
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

volume_count = len(response['result']['volumes'])
sum_bstqos = 0
sum_maxqos = 0
sum_minqos = 0

for i in range(0,volume_count):
        sum_bstqos += response['result']['volumes'][i]['qos']['burstIOPS']
        sum_maxqos += response['result']['volumes'][i]['qos']['maxIOPS']
        sum_minqos += response['result']['volumes'][i]['qos']['minIOPS']

response['result'].update({"sumBurstQoS":sum_bstqos})
response['result'].update({"sumMaxQoS":sum_maxqos})
response['result'].update({"sumMinQoS":sum_minqos})

dump_response = json.dumps(response)
print dump_response

