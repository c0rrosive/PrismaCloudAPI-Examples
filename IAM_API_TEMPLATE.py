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


def get_query_from_id(alert_id):
    endpoint = "/api/v1/permission/alert/search"
    url = build_url(endpoint)
    headers = login_prisma()
    querystring = {"alertId": alert_id }
    response = requests.request("GET", url, headers=headers, params=querystring)
    return(str(response.json()['query']))

def get_permissions(query):
    endpoint = "/api/v1/permission"
    url = build_url(endpoint)
    headers = login_prisma()
    payload = {"limit": 100,"query": query}
    response = requests.request("POST", url, json=payload, headers=headers)
    return(response.text)

get_permissions(get_query_from_id('I-3129830'))
jobject = json.loads(test_response)
print(json.dumps(jobject, indent = 4, ))
