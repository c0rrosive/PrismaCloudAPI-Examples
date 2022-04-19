import requests
import json

base_url = "api3.prismacloud.io"

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
    print('Prisma ID: ' + (((json.loads(response.text))['customerNames'])[0])['prismaId'])
    headers = {'Content-Type': 'application/json', 'x-redlock-auth': token['token']}
    prismaId = (((json.loads(response.text))['customerNames'])[0])['prismaId']
    return(headers, prismaId)

def get_integrations():
    headers, prismaId = login_prisma()
    endpoint = "/api/v1/tenant/" + prismaId + "/integration"
    url = build_url(endpoint)
    querystring = {"type":"splunk", "onlyEnabled":"true"}
    response = requests.request("GET", url, headers=headers, params=querystring)
    print("\n###########################\n")
    print(response)
    print("\n###########################\n")
    print(response.text)
    print("\n###########################\n")
