import requests
import time

base_url = "api.prismacloud.io"

def build_url(endpoint):
    final_url = "https://" + base_url + endpoint
    return(final_url)

def write_file(data):
    with open('script_output.txt', 'w') as outfile:
        outfile.write(data)

def login_prisma():
    endpoint = "/login"
    url = build_url(endpoint)
    payload = "{\"username\":\"ACCESS_KEY\",\"password\":\"SECRET_KEY\"}" # cloud admin
    headers = {"Accept": "application/json; charset=UTF-8","Content-Type": "application/json; charset=UTF-8"}
    response = requests.request("POST", url, data=payload, headers=headers)
    token = response.json()
    #print(token['token'])
    headers = {'Content-Type': 'application/json', 'x-redlock-auth': token['token']}
    return(headers)

def file_write(data):
    filename = alert_id + ".json"
    with open(filename, 'w') as outfile:
        outfile.write(data)

def get_detailed_alert(alert_id):
    endpoint = "/v2/alert/"
    url = build_url(endpoint)
    request_url = url + alert_id + "?detailed=true"
    response = requests.request("GET", request_url, headers=headers)
    print(response)
    print(response.text)
    file_write(response.text)
    time.sleep(1)

alert_list = [P-435083,P-18409,P-9166]

headers = login_prisma()

for alert_id in alert_list:
    get_detailed_alert(alert_id)
