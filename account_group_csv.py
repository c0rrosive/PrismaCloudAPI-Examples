import requests
import time
import json
import re

base_url = "api.prismacloud.io"

def build_url(endpoint):
    final_url = "https://" + base_url + endpoint
    return(final_url)

def file_write(data, filename):
    with open(filename, 'w') as outfile:
        outfile.write(data)

def clean_name(name):
    clean = re.sub('[\s+\/]', '_', name)
    return(clean)


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

def post_csv_request(acct_group):
    endpoint = "/alert/csv"
    url = build_url(endpoint)
    headers = login_prisma()
    payload = {"detailed":True,"filters":[{"name":"timeRange.type","operator":"=","value":"ALERT_OPENED"},{"name":"alert.status","operator":"=","value":"open"},{"name":"account.group","operator":"=","value": acct_group }],"timeRange":{"type":"relative","value":{"amount":"3","unit":"month"}}}
    print(payload)
    print("\n###########################\n")
    response = requests.request("POST", url, json=payload, headers=headers)
    id = (response.json()['id'])
    time.sleep(30)
    return(id)


def get_csv_job(id, acct_group):
    endpoint = "/alert/csv/"
    url = build_url(endpoint) + id + "/download"
    headers = login_prisma()
    response = requests.request("GET", url, headers=headers)
    filename = (str(acct_group) + ".csv")
    file_write(response.text, filename)
    #return(response.text)

def extract_names(group_list):
    names = []
    for i in (group_list):
        names.append(i['name'])
    return(names)

def get_acct_groups():
     endpoint = "/cloud/group/name"
     url = build_url(endpoint)
     querystring = {"include_auto_created":False}
     headers = login_prisma()
     response = requests.request("GET", url, headers=headers, params=querystring)
     group_list = (json.loads(response.text))
     names = extract_names(group_list)
     return(names)

def cycle_list():
    for acct_group in (get_acct_groups()):
        get_csv_job(post_csv_request(acct_group), clean_name(acct_group))


cycle_list()
