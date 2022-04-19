import requests

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
    return(headers)


def post_alert_24_hour_changes_no_filters():
    endpoint = "/v2/alert"
    url = build_url(endpoint)
    headers = login_prisma()
    payload = {"detailed": "True","timeRange": {"type": "relative","value": {"amount": 1, "unit": "day"}},"timeRangeType":"ALERT_UPDATED"}
    response = requests.request("POST", url, json=payload, headers=headers)
    print(response.text)
