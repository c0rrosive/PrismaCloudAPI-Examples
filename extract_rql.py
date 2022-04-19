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
    headers = {'Content-Type': 'application/json', 'x-redlock-auth': token['token']}
    return(headers)

def get_policy():
    endpoint = "/v2/policy"
    url = build_url(endpoint)
    headers = login_prisma()
    querystring = {"policy.name":"AWS API Gateway Rest API attached WAFv2 WebACL is not configured with AMR for Log4j Vulnerability"}
    response = requests.request("GET", url, headers=headers, params=querystring)
    uuid = (response.json()[0]['rule']['criteria'])
    return(uuid)

def get_search_uuid(search_uuid):
    endpoint = "/search/history/" + search_uuid
    url = build_url(endpoint)
    headers = login_prisma()
    response = requests.request("GET", url, headers=headers)
    print(response.json()['query'])

get_search_uuid(get_policy())

    querystring = {"policy.name":"SOME_STRING_VALUE","policy.severity":"SOME_STRING_VALUE","policy.label":"SOME_STRING_VALUE","policy.rule.type":"SOME_STRING_VALUE","policy.subtype":"SOME_STRING_VALUE","policy.type":"SOME_STRING_VALUE","policy.complianceStandard":"SOME_STRING_VALUE","policy.complianceRequirement":"SOME_STRING_VALUE","policy.complianceSection":"SOME_STRING_VALUE","policy.enabled":"SOME_STRING_VALUE","policy.policyMode":"SOME_STRING_VALUE","policy.remediable":"SOME_STRING_VALUE","cloud.type":"SOME_STRING_VALUE"}
