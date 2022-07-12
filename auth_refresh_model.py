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

def get_detailed_alert(alert_id):
    endpoint = "/v2/alert"
    url = build_url(endpoint)
    headers = get_token()
    querystring = {"timeType":"relative","timeAmount":"1","timeUnit":"year","detailed":"True","alert.id": alert_id }
    response = requests.request("GET", url, headers=headers, params=querystring)
    print(response)
    print('################\nCall Time: ' + str(datetime.now()) + '\n#########')
    time.sleep(45.5)



alert_list = ['I-3602030','I-3602028','I-3601949','I-3602056','I-3587084','I-3587083','I-3587078','I-3587077','I-3587074','I-3587073','I-3587088','I-3587087','I-3587089','I-3587091','I-3587090','I-3587093','I-3587092','I-3587076','I-3587075','I-3587094','I-3587082','I-3587081','I-3587080','I-3587079','I-3587086','I-3587085','I-3587171','I-3587169','I-3586948','I-3587072','I-3587168','I-3586950','I-3586949','I-3586945','I-3587170','I-3586944','I-3586937','I-3587022','I-3587021','I-3587167','I-3587019','I-3587020','I-3587018','I-3586947','I-3587017','I-3586946','I-3587166','I-3587165','I-3587164','I-3587162','I-3587163','I-3587159','I-3587161','I-3587160','I-3586943','I-3587016','I-3586942','I-3587015','I-3586941','I-3586940','I-3587014','I-3587013','I-3586939','I-3587010','I-3587012','I-3587011','I-3587009','I-3586938','I-3587008','I-3587158','I-3587157','I-3586936','I-3587007','I-3587006','I-3587154','I-3587155','I-3587153','I-3586851','I-3586935','I-3586850','I-3587005','I-3586934','I-3587004','I-3587003','I-3586848','I-3586849','I-3587001','I-3586847','I-3587000','I-3586846','I-3586932','I-3586845','I-3586844','I-3586843','I-3587071','I-3587070','I-3587069','I-3586999','I-3586931','I-3586997','I-3586998','I-3586929','I-3587068','I-3586928','I-3586842','I-3586841','I-3587067','I-3586927','I-3587066','I-3586996','I-3586840','I-3587065','I-3586926','I-3586925','I-3586995','I-3586994','I-3586924','I-3586993','I-3537268','I-3509288','I-3509020','I-3509019','I-3503882','I-3503953','I-3503651','I-3499585','I-3495459','I-3495394','I-3495391','I-3495390','I-3495389','I-3495388','I-3495387','I-3495386','I-3495312','I-3495557','I-3495556','I-3495311','I-3495458','I-3495457','I-3495456','I-3495310','I-3495151','I-3495150','I-3495149','I-3495393','I-3495392','I-3495553','I-3495555','I-3495554','I-3495385','I-3495309','I-3495384','I-3495308','I-3495454','I-3495453','I-3495148','I-3495307','I-3495251','I-3495250','I-3495382','I-3495249','I-3495248','I-3495247','I-3484173','I-3471024','I-3471268','I-3471022','I-3454080','I-3447546','I-3447616','I-3443451','I-3443692','I-3443504','I-3443617','I-3434511','I-3434435','I-3425274','I-3425265','I-3372219','I-3372281','I-3372362','I-3372215','I-3335727','I-3336017','I-3336016','I-2142590']


def cycle_alerts():
    for alert_id in (alert_list):
        get_detailed_alert(alert_id)

cycle_alerts()
print('################\nDone ' + str(datetime.now()) )
