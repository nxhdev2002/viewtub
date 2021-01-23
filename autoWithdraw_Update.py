import requests
hd ={
    'authorization': 'Bearer ' + requests.get("http://nxhdev.pro/api/hana/token.php?name=" + input("name")).json()['token'], 
    'Content-Type': 'application/json'
}
r = requests.get("https://admin.amaiteam.com/farmer/api/v1/viewtub/account", headers=hd)
print(r.json())
import time
import json
for i in r.json()['data']:

    # r = requests.post("https://admin.amaiteam.com/farmer/api/v1/viewtub/update-account/" + str(i['id']), headers=hd)
    # print (r.text)
# #     # time.sleep(4)
    # data = {
    #     'account_id': i['id'],
    #     'money': i['coin'],
    #     'password': 'xuan6789'
    # }
    # if (i['coin'] > 0):
    #     r = requests.post("https://admin.amaiteam.com/farmer/api/v1/farmer/process-withdrawal-money-viewtub", data=json.dumps(data), headers=hd)
    #     print(r.text)

    r = requests.delete("https://admin.amaiteam.com/farmer/api/v1/viewtub/account/" + str(i['id']) + "?password=xuan6789", headers=hd)
    print(r.text)