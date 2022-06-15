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


def login_prisma_CCS():
    endpoint = "/login"
    url = build_url(endpoint)
    payload = "{\"username\":\"ACCESS_KEY\",\"password\":\"SECRET_KEY\"}" # cloud admin
    headers = {"Accept": "application/json; charset=UTF-8","Content-Type": "application/json; charset=UTF-8"}
    response = requests.request("POST", url, data=payload, headers=headers)
    token = response.json()
    #print(token['token'])
    headers = {'Content-Type': 'application/json', 'authorization': token['token']}
    #print(response.text)
    return(headers)


def get_repos():
    endpoint = "/code/api/v1/repositories"
    url = build_url(endpoint)
    querystring = {"errorsCount":True}
    headers = login_prisma_CCS()
    response = requests.request("GET", url, headers=headers, params=querystring)
    file_write(response.text, 'repos.json')



def get_secrets_errors():
    querystring = {"limit":"SOME_NUMBER_VALUE","offset":"SOME_NUMBER_VALUE"}
    endpoint = "/code/api/v1/errors/file"
    url = build_url(endpoint)
    headers = login_prisma_CCS()
    payload = {
        "repository": "string",
        "sourceTypes": ["Github"],
        "categories": ["Secrets"],
        "types": ["Errors"],
        },
        "filePath": "string"
    }
    response = requests.request("POST", url, json=payload, headers=headers, params=querystring)
    print(response.text)


def list_files_secrets(repo):
    payload = {
        "repository": repo,
        "sourceTypes": ["Github"],
        "categories": ["IAM"],
        "types": ["Errors"],
        "search": {
            "text": "string",
            "options": ["path"],
            "title": "title"
        },
        "authors": ["string"],
        "codeStatus": ["hasFix"]
    }
    endpoint = "/code/api/v1/errors/files"
    url = build_url(endpoint)
    headers = login_prisma_CCS()
    response = requests.request("POST", url, json=payload, headers=headers)
