import requests
import time

base_url = "api.prismacloud.io"

def build_url(endpoint):
    final_url = "https://" + base_url + endpoint
    return(final_url)
    
    
def login_prisma():
    endpoint = "/login"
    url = build_url(endpoint)
    payload = "{\"username\":\"ACCESS_KEY\",\"password\":\"SECRET_KEY\",\"customerName\":\"TENANT_NAME\"}"
    headers = {"Accept": "application/json; charset=UTF-8","Content-Type": "application/json; charset=UTF-8"}
    response = requests.request("POST", url, data=payload, headers=headers)
    token = response.json()
    #print(token['token'])
    headers = {'Content-Type': 'application/json', 'x-redlock-auth': token['token']}
    return(headers)
    
payload =  {"query":"config from cloud.resource where api.name = 'aws-ec2-describe-instances' addcolumn instanceId $.tags[*]","timeRange":{"type":"relative","value":{"unit":"hour","amount":96}}}

def get_query(payload):
    headers = login_prisma()
    endpoint = "/search/config"
    url = build_url(endpoint)
    #payload = {"query":"config where api.name = 'aws-iam-get-account-summary' ","timeRange":{"type":"relative","value":{"unit":"hour","amount":24}}}
    response = requests.request("POST", url, headers=headers, json=payload)
    print("\n###########################\n")
    print(response)
    print("\n###########################\n")
    print(response.text)
    print("\n###########################\n")

get_query(payload)