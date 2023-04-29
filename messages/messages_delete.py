import requests
import time

myid = ""

time_before_month = 4
time_before_day = 14
time_before_year = 2023

token = ""

channel_id = ""
guild_id = ""

delay = 1

headers = {
        "Authorization": token,
        "Origin": "https://discord.com"
}

def parse_res(data):

    if type(data) != list:
        return
    
    print("Get " + str(len(data)))

    print("Current: " + str(data[-1]["timestamp"]))

    for message in data:
        id = message["author"]["id"]

        timestamp = message["timestamp"]
        timestamp = timestamp.split("T")[0]
        timestamp_year = int(timestamp.split("-")[0])
        timestamp_month = int(timestamp.split("-")[1])
        timestamp_day = int(timestamp.split("-")[2])

        if timestamp_year >= time_before_year:
            if timestamp_month > time_before_month:
                return
            if timestamp_month == time_before_month:
                if timestamp_day >= time_before_day:
                    return
            
        #print("pass")
        #return


        if id == myid:
            print("Delete " + str(timestamp_month) + "/" + str(timestamp_day) + " https://discord.com/channels/" + str(message["channel_id"]) + "/" + str(message["id"]))

            headers_a = {
                "Authorization": token,
                "Origin": "https://discord.com",
                "Referer": "https://discord.com/channels/" + guild_id + "/" + message["id"]
            }

            res = requests.delete("https://discord.com/api/v9/channels/" + channel_id + "/messages/" + message["id"], headers=headers_a)

            print(res.status_code)

            time.sleep(delay)
    
    

def download_message(channel_id):

  

    res = requests.get("https://discord.com/api/v9/channels/" + channel_id + "/messages?limit=50", headers=headers)
    res = res.json()

    try:
        parse_res(res)
    except:
       print("Parse error")

    if len(res) == 50:
        time.sleep(delay)
        download_message_before(channel_id, res[-1]["id"])

def download_message_before(channel_id, id):

    

    res = requests.get("https://discord.com/api/v9/channels/" + channel_id + "/messages?before=" + id + "&limit=50", headers=headers)
    res = res.json()
    
    try:
        parse_res(res)
    except:
        print("Parse error")

    if len(res) == 50:
        time.sleep(delay)
        download_message_before(channel_id, res[-1]["id"])



def delete_message_guild(f):
    file = open(f, "r")
    for line in file:
        if line != "" and line != "\n":
            print("Channel: " + line)
            download_message(line.replace("\n", ""))
            time.sleep(1)

#download_message(channel_id)

delete_message_guild("guilds_ids.txt")




