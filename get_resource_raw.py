
import requests
import time

base_url = "api.prismacloud.io"

def build_url(endpoint):
    final_url = "https://" + base_url + endpoint
    return(final_url)

def login_prisma():
    endpoint = "/login"
    url = build_url(endpoint)
    payload = "{\"username\":\"ACCESS_KEY\",\"password\":\"SECRET_KEY\"}"
    headers = {"Accept": "application/json; charset=UTF-8","Content-Type": "application/json; charset=UTF-8"}
    response = requests.request("POST", url, data=payload, headers=headers)
    token = response.json()
    #print(token['token'])
    headers = {'Content-Type': 'application/json', 'x-redlock-auth': token['token']}
    print(response.text)
    return(headers)

def get_absolute_time():
    headers = login_prisma()
    endpoint = "/v2/alert"
    url = build_url(endpoint)
    payload = {"timeRange": {"type": "absolute", "value": {"startTime": 1610581190000,"endTime": 1644795590000}}, "filters": [{ "name": "timeRange.type", "operator": "=", "value": "ALERT_UPDATED"}]}
    response = requests.request('POST', url, headers=headers, json=payload)
    print(response.text)

def get_detailed_alert(alert_id):
    endpoint = "/alert/"
    url = build_url(endpoint)
    print(alert_id)
    request_url = url + alert_id + "?detailed=true"
    headers = login_prisma()
    print(request_url)
    response = requests.request("GET", request_url, headers=headers)
    tags = (response.json()['resource']['data']['tags'])
    print(tags)
    rrn = (response.json()['resource']['rrn'])
    print(rrn)
    return(rrn)

def post_resource_raw(rrn ,id):
    endpoint = "/resource/raw"
    url = build_url(endpoint)
    payload = { "rrn": rrn, "timelineItemId": id }
    print(payload)
    headers = login_prisma()
    response = requests.request("POST", url, json=payload, headers=headers)
    print(response.json()['tags'])
    tags = (response.json()['tags'])
    return(tags)

def post_resource_timeline(rrn):
    endpoint = "/resource/timeline"
    url = build_url(endpoint)
    payload = { "rrn": rrn }
    print(payload)
    headers = login_prisma()
    response = requests.request("POST", url, json=payload, headers=headers)
    id = (response.json()[0]['id'])
    print("\ntimelineid :" + id )
    return(id)

post_resource_raw(get_detailed_alert(alert_id),(post_resource_timeline(get_detailed_alert(alert_id))))
