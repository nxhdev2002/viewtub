import json,requests, time, urllib3, random, string, re,jwt
urllib3.disable_warnings()


def get_random_string(length):
    letters = string.ascii_lowercase
    result_str = ''.join(random.choice(letters) for i in range(length))
    return result_str

def getRandName():
    r = requests.get("https://www.fakeaddressgenerator.com/All_countries/address/country/Vietnam")
    reg = r"value='(.*?)'\/>"
    name = re.findall(reg, r.text)[0].replace("&nbsp;", ' ').split(" ")
    return name

def getToken(token):
    hd = {'authorization': 'Bearer ' + token}
    r = requests.post("https://viewtub.amai-team.com/api/v1/farmer/token",headers=hd, data={}, verify=0)
    return r.json()['data']['token']

def getJWT():
    encoded_jwt = jwt.encode({
        "iss": "https://accounts.google.com",
        "azp": f"74426627020-{get_random_string(32)}.apps.googleusercontent.com",
        "aud": f"74426627020-{get_random_string(32)}.apps.googleusercontent.com",
        "sub": "101851067547615818903",
        "hd": "gmail.com",
        "email": f"{name[0].lower()}{name[2].lower()}{str(random.randint(23,12002))}@gmail.com",
        "email_verified": 1,
        "name": name[0] + " " + name[1] + " " + name[2],
        "picture": "https://lh4.googleusercontent.com/-07LtuJQUyNY/AAAAAAAAAAI/AAAAAAAAAAA/AMZuucnonlC5ZswTJi0jmlIl-EzEFoHygQ/s96-c/photo.jpg",
        "given_name": name[0],
        "family_name": name[2],
        "locale": "en",
        "iat": 1605777700,
        "exp": 1605781832,
        "jti": "d3b39b97-3d1f-4b85-a1ff-ab76d3c0da42"
    }, 'hoangdz20cm', algorithm='HS256')
    return encoded_jwt


def regAcc(social_id, social_name, social_token, social_email):
    
    data=  {
        'social_id': social_id,
        'social_name': social_name,
        'social_avatar': 'https://lh4.googleusercontent.com/-07LtuJQUyNY/AAAAAAAAAAI/AAAAAAAAAAA/AMZuucnonlC5ZswTJi0jmlIl-EzEFoHygQ/s96-c/photo.jpg',
        'social_token': social_token,
        'social_email': social_email

    }
    r = requests.post("https://viewtub.amai-team.com/api/v1/auth/callback/google/login", data=data, headers={'user-agent':'okhttp/3.12.1'}, verify=0)
    print (r.json()['data']['access_token'])
    return r.json()['data']['access_token']

def add2Hana(token, name):
    r = requests.post("https://admin.amaiteam.com/farmer/api/v1/viewtub/add", data={'token': token}, headers={'authorization': 'Bearer ' + requests.get("http://nxhdev.pro/api/hana/token.php?name=" + name).json()['token']})
    return (r.text)

def add2DB(token, param, owner):
    data = {
        'token': token,
        'name': name[0] + " " + name[1] + " " + name[2],
        'owner': owner,
        'reg_params': param
    }
    r = requests.post("http://nxhdev.pro/api/viewTub/index.php", data=data)
    return r.json()

if __name__ == "__main__":
    username = input("name: ")
    while (True):
        try:
            name = getRandName()

            social_id = get_random_string(28)
            social_name = name[0] + " " + name[1]
            social_token = getJWT()
            social_email = f"{name[0]}{name[1]}{get_random_string(random.randint(1,4))}{str(random.randint(32, 9999))}@gmail.com"

            param = f"{social_id}|{social_name}|{social_token}|{social_email}"

            token_google = regAcc(social_id,social_name,social_token,social_email)
            token = getToken(token_google)
            print(add2Hana(token, username))
            print(add2DB(token_google, param, username))
        except:
            pass