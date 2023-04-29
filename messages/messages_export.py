import json
import os
import base64

def base64_decode(s):
    return base64.b64decode(s.encode("utf-8")).decode("utf-8")

guild_id = ""

if not os.path.exists("export"): os.mkdir("export")
if not os.path.exists("export/" + guild_id): os.mkdir("export/" + guild_id)

for name in os.listdir("data/" + guild_id):
    if "info" in name:
        file = open("data/" + guild_id + "/" + name, "r")
        data = file.readline()
        file.close()

        data = json.loads(data)

        file = open("export/" + guild_id + "/info", "w")

        for channel in data["channels"]:
            file.write(channel["id"] + "\t" + channel["name"] + "\n")
        
        file.flush()
        file.close()
    
    else:
        file = open("data/" + guild_id + "/" + name, "r")
        file_export = open("export/" + guild_id + "/" + name, "w")

        for line in file.readlines():
            data = base64_decode(line)
            data = json.loads(data)
            
            for message in data:
                l = ""

                l += message["id"] + ":"
                l += message["timestamp"].replace("T", " ").split(".")[0] + ": ("
                l += message["author"]["id"] + ":"
                l += message["author"]["username"] + ") :"
                
                if message["content"] != "":
                    l += message["content"] + ":"

                if len(message["embeds"]) >= 1:
                    l += json.dumps(message["embeds"]) + ":"

                if len(message["attachments"]) >= 1:
                    l += json.dumps(message["attachments"]) + ":"

                file_export.write(l + "\n")

            file_export.flush()

        file.close()
        file_export.close()