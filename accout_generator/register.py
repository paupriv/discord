import random
import requests
import json
import time
import base64
import quopri
import os

domain = "domain.de"
captcha_key = "key"
request_timeout = 500



mail_dic = "mails"
token_file = "tokens.txt"

def get_fingerprint(user_agent):
    headers_fingerprint = {
    "Referer": "https://discord.com/register",
    "User-Agent": user_agent
    }

    fingerprint = requests.get(url="https://discord.com/api/v9/experiments", headers=headers_fingerprint)

    return fingerprint.json()["fingerprint"]

def randomUserAgent():
    # Do
    return "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.5414.120 Safari/537.36"

def randomSuperProperties(user_agent):
    s = "{\"os\":\"Windows\",\"browser\":\"Chrome\",\"device\":\"\",\"system_locale\":\"en-US\",\"browser_user_agent\":\"" + user_agent + "\",\"browser_version\":\"109.0.5414.120\",\"os_version\":\"10\",\"referrer\":\"\",\"referring_domain\":\"\",\"referrer_current\":\"\",\"referring_domain_current\":\"\",\"release_channel\":\"stable\",\"client_build_number\":9999,\"client_event_source\":null}"

    return base64.b64encode(s.encode("ascii")).decode("ascii")

def randomPassword():
    return ''.join(random.choice("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!") for i in range(10)) + '!'

def randomName():
    return ''.join(random.choice("abcdefghijklmnopqrstuvwxyz") for i in range(8))

def randomBirthDay():
    t = ""
    r = ""
    r += str(random.randrange(1990, 2000))
    r += "-"
    t = str(random.randrange(1, 12))
    if len(t) == 1:
        t = "0" + t
    r += t
    r += "-"
    t = str(random.randrange(1, 30))
    if len(t) == 1:
        t = "0" + t
    r += t
    return r

proxies_socks5 = []
proxies_http = []

def load_proxies_http():
    global proxies_http

    file = open("proxies/http.txt")
    for line in file:
        line = line.replace("\n", "")
        #if ":" in line:
        #    host = line.split(":")[0]
        #    port = line.split(":")[1]
        #
        #    proxies[host] = port

        proxies_http.append(line)

def load_proxies_socks5():
    global proxies_socks5

    file = open("proxies/socks5.txt")
    for line in file:
        line = line.replace("\n", "")
        #if ":" in line:
        #    host = line.split(":")[0]
        #    port = line.split(":")[1]
        #
        #    proxies[host] = port

        proxies_socks5.append(line)

def randomProxy(type):
    global proxies_http

    if "SOCKS5" == type:
        return "SOCKS5", random.choice(proxies_socks5)
    if "HTTP" == type:
        return "HTTP", random.choice(proxies_http)

def solve_captcha(ss, proxy_type, proxy, pageurl):
    time.sleep(3)

    res_cap_submit = requests.get(url="http://2captcha.com/in.php?key=" + captcha_key + "&method=hcaptcha&sitekey=" + ss + "&proxytype=" + proxy_type + "&proxy=" + proxy + "&pageurl=" + pageurl)
    if "|" not in res_cap_submit.text:
        print("ERROR 2captcha in.php: " + res_cap_submit.text)
    
    id = res_cap_submit.text.split("|")[1]

    while True:
        time.sleep(5)

        res_cap_get = requests.get(url="http://2captcha.com/res.php?key=" + captcha_key + "&action=get&id=" + id)
        if res_cap_get.text != "CAPCHA_NOT_READY":
            break

    print(res_cap_get.text[:64])

    if "ERROR" in res_cap_get.text.upper():
        return ""

    return res_cap_get.text.split("|")[1]

def register():

    password = randomPassword()
    birth_day = randomBirthDay()
    name = randomName()
    email = name + "@" + domain
    
    user_agent = randomUserAgent()
    fingerprint = get_fingerprint(user_agent)

    super_properties = randomSuperProperties(user_agent)

    proxy_type, proxy = randomProxy("SOCKS5")

    proxy_use = dict(
        http=proxy_type.lower() + '://' + proxy,
        https=proxy_type.lower() + '://' + proxy
    )

    print("Data " + email + " " + name + " " + password + " " + birth_day)

    data_try = {
        "X-Super-Properties": super_properties,
        "fingerprint": fingerprint,
        "email": email,
        "username": name,
        "password": password,
        "invite": "null",
        "consent": "true",
        "date_of_birth": birth_day,
        "gift_code_sku_id": "null",
        "captcha_key": "null",
        "promotional_email_opt_in": "false"
    }

    headers_try = {
        "Referer": "https://discord.com/register",
        "Content-Type": "application/json",
        #"Content-Length": str(len(data)),
        "User-Agent": user_agent
    }

    res_try = requests.post(url="https://discord.com/api/v9/auth/register", json=data_try, headers=headers_try, proxies=proxy_use, timeout=request_timeout)
    
    if "retry_after" in res_try.text:
        print("Wait before try again " + str(res_try.json()["retry_after"]))
        return

    token = ""

    j = res_try.json()

    if "captcha_sitekey" in res_try.text:
        site_key = j["captcha_sitekey"]

        while True:
            
            print("Submit cap")
            key = solve_captcha(site_key, proxy_type, proxy, "https://discord.com/api/v9/auth/register")

            if key == "":
                return


            data_reg = {
                "fingerprint": fingerprint,
                "email": email,
                "username": name,
                "password": password,
                "invite": "null",
                "consent": "true",
                "date_of_birth": birth_day,
                "gift_code_sku_id": "null",
                "captcha_key": key,
                "promotional_email_opt_in": "false"
            }

            headers_reg = {
                "X-Super-Properties": super_properties,
                "Referer": "https://discord.com/register",
                "Content-Type": "application/json",
                "Content-Length": str(len(str(data_reg))),
                "User-Agent": user_agent,
                "X-Fingerprint": fingerprint,
                "X-Debug-Options": "bugReporterEnabled",
                "Sec-Ch-Ua-Mobile": "?0",
                "X-Discord-Locale": "en-US",
                "Sec-Ch-Ua": "\"Chromium\";v=\"109\", \"Not_A Brand\";v=\"99\"",
                "Sec-Ch-Ua-Platform": "Linux",
                "Sec-Fetch-Site": "same-origin",
                "Sec-Fetch-Mode": "cors",
                "Sec-Fetch-Dest": "empty",
                "Origin": "https://discord.com"
            }

            res_reg = requests.post(url="https://discord.com/api/v9/auth/register", json=data_reg, headers=headers_reg, proxies=proxy_use, timeout=request_timeout)
            #res_reg = requests.post(url="http://localhost:8888/api/v9/auth/register", json=data_reg, headers=headers_reg)

            #print(res_reg.text)
            
            if "captcha_sitekey" in res_reg.text:
                site_key = res_reg.json()["captcha_sitekey"]
            else:
                token = res_reg.json()["token"]
                break

    elif "token" in j:
        token = j["token"]

    if token != "":
        file = open("tokens.txt", "a")
        file.write(token)
        file.write("###")
        file.write(email)
        file.write("###")
        file.write(name)
        file.write("###")
        file.write(password)
        file.write("###")
        file.write(birth_day)
        file.write("###")
        file.write(super_properties)
        file.write("###")
        file.write(fingerprint)
        file.write("###")
        file.write(user_agent)
        file.write("###")
        file.write(proxy)
        file.write("###")
        file.write(proxy_type)

        file.write("\n")
        file.close()
    else:
        print("ERROR token gen")

    #print(len(data))

def verfiy_email():
    for file in os.listdir(mail_dic):
        file_name = mail_dic + "/" + file
        dec = base64.b64decode(file.encode('ascii')).decode('ascii')
        if " " in dec:
            dec = dec.split(" ")[1]

        email = dec
    
        s = ""
        a = False

        f = open(file_name, "r")
        for line in f:
            if "--" in line and not a:
                a = True
            elif "--" in line and a:
                a = False
                if "https" in s and "discord" in s:
                    break
                s = ""

            if a:
                s += line
    
        s = s[s.index("https"):]
    
        if "\"" in s:
            s = s[0:s.index('\"')]

        decoded = quopri.decodestring(s.encode('utf-8')).decode('utf-8').replace("\n", "")

        tokens = open(token_file)
        for line in tokens:
            if "###" in line:
                if line.split("###")[1] in email:
                    line = line[0:line.index('\n')]

                    super_properties = line.split("###")[5]
                    fingerprint = line.split("###")[6]
                    user_agent = line.split("###")[7]
                    proxy = line.split("###")[8]
                    proxy_type = line.split("###")[9]

                    #proxy_type = proxy_type[0:proxy_type.index('\n')]

                    #print(proxy)
                    #print(proxy_type)

                    proxy_use = dict(
                        http=proxy_type.lower() + '://' + proxy,
                        https=proxy_type.lower() + '://' + proxy
                    )

                    headers = {
                        "User-Agent": user_agent
                    }

                    res = requests.get(url=decoded, headers=headers, proxies=proxy_use, allow_redirects=False)
    
                    loc = res.headers["Location"]

                    token = loc.split("=")[1]

                    print(token)

                    data_try = {
                        "token": token,
                        "captcha_key": "null"
                    }

                    headers_try = {
                        "X-Fingerprint": fingerprint,
                        "X-Super-Properties": super_properties,
                        #"Referer": "https://discord.com/register",
                        "Content-Type": "application/json",
        #"Content-Length": str(len(data)),
                        "User-Agent": user_agent
                    }

                    res_try = requests.post(url="https://discord.com/api/v9/auth/verify", json=data_try, headers=headers_try, proxies=proxy_use, timeout=request_timeout)
    
                    if "retry_after" in res_try.text:
                        print("Wait before try again " + str(res_try.json()["retry_after"]))
                        return

                    user_id = ""
                    new_token = ""

                    j = res_try.json()

                    if "captcha_sitekey" in res_try.text:
                        site_key = j["captcha_sitekey"]

                        while True:
            
                            print("Submit cap")
                            key = solve_captcha(site_key, proxy_type, proxy, "https://discord.com/api/v9/auth/verify")

                            if key == "":
                                return

                            data_reg = {
                                "token": token,
                                "captcha_key": key
                            }

                            headers_reg = {
                                "X-Fingerprint": fingerprint,
                                "X-Super-Properties": super_properties,
                                #"Referer": "https://discord.com/register",
                                "Content-Type": "application/json",
        #"Content-Length": str(len(data)),
                                "User-Agent": user_agent
                            }

                            res_reg = requests.post(url="https://discord.com/api/v9/auth/verify", json=data_reg, headers=headers_reg, proxies=proxy_use, timeout=request_timeout)
    

            
                            if "captcha_sitekey" in res_reg.text:
                                site_key = res_reg.json()["captcha_sitekey"]
                            else:
                                user_id = res_reg.json()["user_id"]
                                new_token = res_reg.json()["token"]
                                break

                    elif "user_id" in j:
                        user_id = j["user_id"]
                        new_token = j["token"]

                    line = new_token + "###" + line + "###" + user_id

                    file = open("verify_email.txt", "a")
                    file.write(line)
                    file.write("\n")
                    file.close()
                    
def verify_number():
    file = open("verify_email.txt")

    for line in file:
        if "###" in line:
            line = line[0:line.index('\n')]
                #super_properties = line.split("###")[5]
                #fingerprint = line.split("###")[6]
                
            token = line.split("###")[0]
            user_agent = line.split("###")[8]
            proxy = line.split("###")[9]
            proxy_type = line.split("###")[10]

                    #proxy_type = proxy_type[0:proxy_type.index('\n')]

                    #print(proxy)
                    #print(proxy_type)

            proxy_use = dict(
                http=proxy_type.lower() + '://' + proxy,
                https=proxy_type.lower() + '://' + proxy
            )

            headers = {
                "User-Agent": user_agent,
                "Authorization": token
            }

            res = requests.get(url="https://discord.com/api/v9/users/@me/affinities/users", headers=headers, proxies=proxy_use)

            if "verify your account" in res.text:
                print("F")




load_proxies_socks5()

#print(randomProxy("http"))
#print(randomProp("w"))

#register()


#print(get_fingerprint(randomUserAgent()))

#verfiy_email()

verify_number()
