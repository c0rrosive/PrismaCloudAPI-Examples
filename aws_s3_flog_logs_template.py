import requests

base_url = "api2.prismacloud.io"

def build_url(endpoint):
    final_url = "https://" + base_url + endpoint
    return(final_url)

def login_prisma():
    endpoint = "/login"
    url = build_url(endpoint)
    payload = "{\"username\":\"ACCESS_KEY\",\"password\":\"SECRET_KEY\"}" # cloud admin
    headers = {"Accept": "application/json; charset=UTF-8","Content-Type": "application/json; charset=UTF-8"}
    response = requests.request("POST", url, data=payload, headers=headers)
    token = response.json()
    #print(token['token'])
    headers = {'Content-Type': 'application/json', 'x-redlock-auth': token['token']}
    #print(response.text)
    return(headers)


def get_cloud_account_names(cloudtype):
    querystring = {"onlyActive":True,"cloudType":cloudtype}
    endpoint = "/cloud/name"
    url = build_url(endpoint)
    headers = login_prisma()
    response = requests.request("GET", url, headers=headers, params=querystring)
    print(response.text)


def get_flow_log_config(cloud_account_id):
    endpoint = "/cloud-accounts-manager/v1/cloud-accounts/aws/" + cloud_account_id + "/features/aws-flow-logs/s3"
    url = build_url(endpoint)
    headers = login_prisma()
    response = requests.request("GET", url, headers=headers)
    print(response.text)


def validate_flow_log_config(cloud_account_id, bucket_name, logging_account_id):
    endpoint = "/cloud-accounts-manager/v1/cloud-accounts/aws/" + cloud_account_id + "/features/aws-flow-logs/s3/status"
    url = build_url(endpoint)
    headers = login_prisma()
    payload = {"loggingAccountId": logging_account_id ,"awsS3FlowLogsLoggingAccountId": 0,"buckets": [ bucket_name  ],"bucketIds": [0]}
    response = requests.request("POST", url, headers=headers, json=payload)
    print(payload)
    print(response)
    print(response.text)

def patch_flow_log_config(logging_account_id, bucket_name, cloud_account_id):
    endpoint = "/cloud-accounts-manager/v1/cloud-accounts/aws/" + cloud_account_id + "/features/aws-flow-logs/s3"
    url = build_url(endpoint)
    headers = login_prisma()
    payload = {"loggingAccounts": [{"buckets": [ bucket_name ],"loggingAccountId": logging_account_id}]}
    response = requests.request("PATCH", url, headers=headers, json=payload)
    print(payload)
    print(response)
    print(response.text)


#example:
get_cloud_account_names('aws')
 get_flow_log_config('870386726947')
{"loggingAccounts":[{"loggingAccountId":"870386726947","buckets":["testing-prisma-test-bucket"]}]}
 patch_flow_log_config('870386726947','testing-prisma-test-bucket','870386726947')
{'loggingAccounts': [{'buckets': ['testing-prisma-test-bucket'], 'loggingAccountId': '870386726947'}]}
<Response [201]>
