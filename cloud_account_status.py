import requests

base_url = "api.prismacloud.io"

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
    print(response.text)
    return(headers)


def get_cloud_status_id(account_id):
    endpoint = "/account/" + account_id + "/config/status"
    url = build_url(endpoint)
    headers = login_prisma()
    response = requests.request("GET", url, headers=headers)
    print(response)
    print(response.text)
