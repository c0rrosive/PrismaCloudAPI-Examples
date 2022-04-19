import requests

base_url = "api.prismacloud.io"

def build_url(endpoint):
    final_url = "https://" + base_url + endpoint
    return(final_url)

def file_write(data, filename):
    with open(filename, 'w') as outfile:
        outfile.write(data)

def login_prisma():
    endpoint = "/login"
    url = build_url(endpoint)
    payload = "{\"username\":\"ACCESS_KEY\",\"password\":\"SECRET_KEY\"}"
    headers = {"Accept": "application/json; charset=UTF-8","Content-Type": "application/json; charset=UTF-8"}
    response = requests.request("POST", url, data=payload, headers=headers)
    token = response.json()
    #print(token['token'])
    headers = {'Content-Type': 'application/json', 'x-redlock-auth': token['token']}
    #print(response.text)
    return(headers)


def get_audit_logs():
    endpoint = "/audit/redlock"
    url = build_url(endpoint)
    headers = login_prisma()
    querystring = {"timeType":"relative","timeAmount":1,"timeUnit":"year"}
    response = requests.request("GET", url, headers=headers, params=querystring)
    file_write(response.text, 'audit_logs.json')
