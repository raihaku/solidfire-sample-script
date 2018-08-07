import json
import warnings
import requests
from requests.packages.urllib3 import exceptions

def solidfire_api(url,endpoint,payload):
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

    return response

endpoint = {}
endpoint['login'] = "admin"
endpoint['passwd'] = "P@ssw0rd"
params = {}

url = 'https://solidfire.mvip/json-rpc/10.1'

drive_payload = {'method': "ListDrives", 'params': params}
ccap_payload = {'method': "GetClusterCapacity", 'params': params}
drive_response = solidfire_api(url,endpoint,drive_payload)
ccap_response = solidfire_api(url,endpoint,ccap_payload)
max_metaused = ccap_response['result']['clusterCapacity']['maxUsedMetadataSpace']
drive_count = len(drive_response['result']['drives'])
list_drive_capacity = []

for i in range(0,drive_count):
        if drive_response['result']['drives'][i]['type'] == 'volume':
                list_drive_capacity.append(drive_response['result']['drives'][i]['capacity'])

largest_drive_capacity = max(list_drive_capacity)
list_drive_capacity.remove(largest_drive_capacity)
second_largest_drive_capacity = max(list_drive_capacity)
warn_metadata = max_metaused - (largest_drive_capacity + second_largest_drive_capacity) * 0.45
ccap_response['result']['clusterCapacity'].update({"warningMetadataThreshold":warn_metadata})
dump_response = json.dumps(ccap_response)
print dump_response

