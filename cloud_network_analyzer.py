import requests
import json

base_url = "api.prismacloud.io"

cns_url = "https://api.east-02.network.prismacloud.io"

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
    print("token:" + token['token'])
    print('Prisma ID: ' + (((json.loads(response.text))['customerNames'])[0])['prismaId'])
    return(token['token'])

def get_cns_token(pc_token):
    endpoint = "/issue"
    url = cns_url + endpoint
    headers = {"Content-Type": "application/json"}
    payload = {"metadata": {"token": pc_token},"realm": "PCIdentityToken","validity": "24h"}
    response = requests.request("POST", url, json=payload, headers=headers)
    print(response.text)
    return(response.text)

#get_cns_token(login_prisma())
def get_cns_header():
    cns_response = get_cns_token(login_prisma())
    prismaId = (json.loads(cns_response)['claims']['data']['prismaid'])
    cns_token = (json.loads(cns_response)['token'])
    cns_header = {'x-namespace': ("/" + prismaId) , 'Authorization': ("Bearer " + cns_token) }
    return(cns_header)
  

def query_cns():
    endpoint = "/cnssearches"
    url = cns_url + endpoint
    payload = {"query":"config from network where source.network = '0.0.0.0/0' and address.match.criteria = 'full_match' and dest.resource.type = 'Instance' and dest.cloud.type = 'AWS' and protocol.ports in ( 'tcp/0:79', 'tcp/81:442', 'tcp/444:65535' )","timeRange": {"type": "to_now","value": "epoch"}}
    response = requests.request("POST", url, json=payload, headers=cns_header)
    print(response.text)

def get_cloudgraph():
    data = """
      {
    "query": {
        "addressMatchCriteria": "NotApplicable",
        "destinationSelector": {
            "cloudTypes": [
                "AWS"
            ],
            "regions": [
                "us-east-2"
            ],
            "resourceType": "Interface"
        },
        "effectiveAction": "Allowed",
        "excludeEnterpriseIPs": true,
        "name": "RQL search",
        "rawRQL":"config from network where source.network = UNTRUST_INTERNET and dest.resource.type = "Interface" and dest.cloud.region = "AWS Ohio"",
        "sourceIP": "0.0.0.0/0",
        "sourceSelector": {
            "resourceType": "Instance"
        },
        "type": "CompressedGraph"
    }
  }
    """
    endpoint = "/cloudgraphs"
    url = cns_url + endpoint
    response = requests.request("POST", url, data=data, headers=cns_header)
    print(response.text) 
