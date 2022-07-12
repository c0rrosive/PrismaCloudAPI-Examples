import requests
import time
import json
from datetime import datetime

base_url = "api.prismacloud.io"

token = ""

token_expiration = ""

token_validity = 540

def build_url(endpoint):
    final_url = "https://" + base_url + endpoint
    return(final_url)

def reset_auth():
    global token
    global token_expiration
    token = ""
    token_expiration = ""
    print('\nAuthentication Token reset ' + str(datetime.now()))

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

def refresh_token(old_token):
    endpoint = "/auth_token/extend"
    url = build_url(endpoint)
    headers = old_token
    response = requests.request("GET", url, headers=headers)
    print(response)
    print(response.text)
    if response.status_code != 200:
        reset_auth()
        get_token()
    else:
        token_response = response.json()['token']
        global token
        global token_expiration
        token = {'Content-Type': 'application/json', 'x-redlock-auth': token_response}
        token_expiration = (int(time.time()) + token_validity)
        print('\nAuthentication Token refreshed ' + str(datetime.now()))

def get_token():
    global token
    global token_expiration
    if (token == ""):
        token = login_prisma()
        token_expiration = (int(time.time()) + token_validity)
        print('\nLogin initialiazed ' + str(datetime.now()))
        return(token)
    else:
        if (token_expiration <= (int(time.time()))):
            refresh_token(token)
            return(token)
        else:
            return(token)


