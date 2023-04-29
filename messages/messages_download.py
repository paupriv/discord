import time
import requests
import os
import websocket
import json
import base64



token = ""
delay = 1

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

def download_message(file, channel_id):

    headers = {
        "Authorization": token
    }

    res = requests.get("https://discord.com/api/v9/channels/" + channel_id + "/messages?limit=50", headers=headers)
    res = res.json()

    file.write(base64_encode(json.dumps(res)))
    file.write("\n")
    file.flush()

    if len(res) == 50:
        time.sleep(delay)
        download_message_before(file, channel_id, res[-1]["id"])

def download_message_before(file, channel_id, id):

    headers = {
        "Authorization": token
    }

    res = requests.get("https://discord.com/api/v9/channels/" + channel_id + "/messages?before=" + id + "&limit=50", headers=headers)
    res = res.json()
    
    file.write(base64_encode(json.dumps(res)))
    file.write("\n")
    file.flush()

    if len(res) == 50:
        time.sleep(delay)
        download_message_before(file, channel_id, res[-1]["id"])

def download_guild():
    guild_id = ""

    if not os.path.exists("data"):
        os.mkdir("data")
    
    if not os.path.exists("data/" + guild_id):
        os.mkdir("data/" + guild_id)
    
    file = open("data.txt", "r")
    data = file.read()
    file.close()

    data = json.loads(data)
    guilds = data["d"]["guilds"]

    guild = None

    for g in guilds:
        if g["id"] == guild_id:
            guild = g
    
    if guild == None:
        return

    file = open("data/" + guild_id + "/info", "w")
    file.write(json.dumps(guild))
    file.write("\n")
    file.flush()
    file.close()

    for channel in guild["channels"]:
        ch_base64 = base64_encode(channel["name"])

        file_path = "data/" + guild_id + "/" + channel["id"]
        if os.path.exists(file_path):
            print("[Channel] Skip " + channel["name"])
            continue

        if "last_message_id" not in channel:
            continue

        print("[Channel] Start download " + channel["name"])

        file = open("data/" + guild_id + "/" + channel["id"], "w")
        #last_message_id = channel["last_message_id"]

        download_message(file, channel["id"])

#receive_data()

download_guild()
