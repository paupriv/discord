import requests
import time
import json

token = ""

headers = {
    "Authorization": token,
    "Content-Type": "application/json",
    "User-Agent": "Mozilla/5.0 (Linux; Android 10; SM-A202F Build/QP1A.190711.020; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/85.0.4183.101 Mobile Safari/537.36 [FB_IAB/FB4A;FBAV/307.0.0.40.111;]"
}

def disable(name):
    file = open(name, "r")

    for line in file.readlines():
        if line != "":
            line = line[0:-1]
            
        id = line
        data = json.loads("{\"recipients\":[\"" + id + "\"]}")

        res = requests.post("https://discord.com/api/v9/users/@me/channels", json=data, headers=headers)
        print(res.status_code)
        # 200 Correct
        # Other, find error

        time.sleep(1)

disable("ids.txt")