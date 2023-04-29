import time
import requests
import os
import websocket
import json
import base64

token = ""
guild_id = ""

delay = 1

def base64_encode(s):
    return base64.b64encode(s.encode("utf-8")).decode("utf-8")

def on_message(wsapp, message):
    if "}" in message:
        if json.loads(message).get("t") == "READY":

            data = json.loads(message)
            guilds = data["d"]["guilds"]

            guild = None

            for g in guilds:
                if g["id"] == guild_id:
                    guild = g
    
            if guild == None:
                return

            file = open("get_channel_ids.txt", "w")
            for channel in guild["channels"]:
                file.write(channel["id"] + "\n")
                file.flush()
            file.close()
            exit(0)


def on_open(ws):
    print("Open")
    init = "{\"op\":2,\"d\":{\"token\":\"" + token + "\",\"capabilities\":4093,\"properties\":{\"os\":\"Windows\",\"browser\":\"Chrome\",\"device\":\"\",\"system_locale\":\"en-US\",\"browser_user_agent\":\"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.5414.120 Safari/537.36\",\"browser_version\":\"109.0.5414.120\",\"os_version\":\"10\",\"referrer\":\"\",\"referring_domain\":\"\",\"referrer_current\":\"\",\"referring_domain_current\":\"\",\"release_channel\":\"stable\",\"client_build_number\":176020,\"client_event_source\":null},\"presence\":{\"status\":\"unknown\",\"since\":0,\"activities\":[],\"afk\":false},\"compress\":false,\"client_state\":{\"guild_versions\":{},\"highest_last_message_id\":\"0\",\"read_state_version\":0,\"user_guild_settings_version\":-1,\"user_settings_version\":-1,\"private_channels_version\":\"0\",\"api_code_version\":0}}}"
    ws.send(init)

def receive_data():
    wsapp = websocket.WebSocketApp("wss://gateway.discord.gg/?encoding=json&v=9", on_message=on_message, on_open=on_open)
    wsapp.run_forever()

        

receive_data()
