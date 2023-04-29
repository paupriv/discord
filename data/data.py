import json
import websocket # websocket-client
import time
import base64
import requests
import sys

sys.setrecursionlimit(200000000)

token = ""

# Utils

def base64_encode(s):
    return base64.b64encode(s.encode("utf-8")).decode("utf-8")

def on_message(wsapp, message):
    if "}" in message:
        if json.loads(message).get("t") == "READY":
            file = open("data.txt", "w")
            file.write(message)
            file.write("\n")
            file.flush()
            file.close()
            wsapp.close()

            print("Data received and saved to data.txt")
def on_open(ws):
    print("Open")
    init = "{\"op\":2,\"d\":{\"token\":\"" + token + "\",\"capabilities\":4093,\"properties\":{\"os\":\"Windows\",\"browser\":\"Chrome\",\"device\":\"\",\"system_locale\":\"en-US\",\"browser_user_agent\":\"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.5414.120 Safari/537.36\",\"browser_version\":\"109.0.5414.120\",\"os_version\":\"10\",\"referrer\":\"\",\"referring_domain\":\"\",\"referrer_current\":\"\",\"referring_domain_current\":\"\",\"release_channel\":\"stable\",\"client_build_number\":176020,\"client_event_source\":null},\"presence\":{\"status\":\"unknown\",\"since\":0,\"activities\":[],\"afk\":false},\"compress\":false,\"client_state\":{\"guild_versions\":{},\"highest_last_message_id\":\"0\",\"read_state_version\":0,\"user_guild_settings_version\":-1,\"user_settings_version\":-1,\"private_channels_version\":\"0\",\"api_code_version\":0}}}"
    ws.send(init)

def receive_data():
    wsapp = websocket.WebSocketApp("wss://gateway.discord.gg/?encoding=json&v=9", on_message=on_message, on_open=on_open)
    wsapp.run_forever()

#receive_data()

def parse_res(guild_id, channel_id, channel_name, data):
    #print("test")

    if type(data) != list:
        return
    for message in data:
        if message["attachments"] == None:
            continue
        for attachment in message["attachments"]:
            id = attachment["id"]
            filename = base64_encode(attachment["filename"])
            size = str(attachment["size"])
            url = attachment["url"]
            content_type = attachment["content_type"]

            file = open("download.txt", "a")
            file.write(guild_id)
            file.write("#")
            file.write(channel_id)
            file.write("#")
            file.write(channel_name)
            file.write("#")
            file.write(id)
            file.write("#")
            file.write(filename)
            file.write("#")
            file.write(size)
            file.write("#")
            file.write(url)
            file.write("#")
            file.write(content_type)
            file.write("\n")
            file.flush()
            file.close()

def download_message(guild_id, channel_id, channel_name):

    headers = {
        "Authorization": token
    }

    res = requests.get("https://discord.com/api/v9/channels/" + channel_id + "/messages?limit=50", headers=headers)
    res = res.json()

    try:
        parse_res(guild_id, channel_id, channel_name, res)
    except:
        print("Parse error")

    if len(res) == 50:
        time.sleep(1)
        download_message_before(guild_id, channel_id, channel_name, res[-1]["id"])

def download_message_before(guild_id, channel_id, channel_name, id):

    headers = {
        "Authorization": token
    }

    res = requests.get("https://discord.com/api/v9/channels/" + channel_id + "/messages?before=" + id + "&limit=50", headers=headers)
    res = res.json()
    
    try:
        parse_res(guild_id, channel_id, channel_name, res)
    except:
        print("Parse error")

    if len(res) == 50:
        time.sleep(1)
        download_message_before(guild_id, channel_id, channel_name, res[-1]["id"])

def parse():
    tmp = open("log_old.txt", "r")
    log = tmp.read()
    tmp.close()

    file = open("data.txt")
    data = file.readline()
    file.close()
    
    data = json.loads(data)
    guilds = data["d"]["guilds"]

    for guild in guilds:
        
# paste guild id here
      
        if guild["id"] == "":
            guild_id = guild["id"]
            for channel in guild["channels"]:
                print("Started " + channel["id"] + " " + channel["name"])

                if channel["name"] != None:
                    channel_name = base64_encode(channel["name"])
                    channel_id = channel["id"]

                    if channel_id in log:
                        print("Skip " + channel_id)
                    else:
                    
                        # TODO Check channel already started, program crash

                        download_message(guild_id, channel_id, channel_name)

                        time.sleep(1)


parse()