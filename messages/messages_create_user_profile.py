import os
import base64
import json
import datetime
import calendar

guild_info = ""

def base64_decode(s):
    return base64.b64decode(s.encode("utf-8")).decode("utf-8")

def decode_channel_id(guild_id, channel_id):
    global guild_info

    if guild_info == "":
        file = open("data/" + guild_id + "/info")
        guild_info = file.read()
        file.close()

        guild_info = json.loads(guild_info)
    
    for c in guild_info["channels"]:
        if c["id"] == channel_id:
            return c["name"]

def activity_user(guild_id, user_id):
    count = 0
    count_by_channels = {}

    count_by_day = {"Monday":0,"Tuesday":0,"Wednesday":0,"Thursday":0,"Friday":0,"Saturday":0,"Sunday":0}

    count_by_hours = {}

    for f in os.listdir("data/" + guild_id):
        if f == "info":
            continue
        file = open("data/" + guild_id + "/" + f, "r")
        for line in file:
            if line == "":
                continue
            data = base64_decode(line)
            try:
                data = json.loads(data)
                for message in data:
                    if message["author"]["id"] == user_id:
                        count += 1
                        channel_id = message["channel_id"]
                        if channel_id in count_by_channels:
                            count_by_channels[channel_id] += 1
                        else:
                            count_by_channels[channel_id] = 1
                        
                        timestamp = message["timestamp"]
                        day = timestamp.split("T")[0]
                        time = timestamp.split("T")[1].split(".")[0]

                        dayy = datetime.datetime(int(day.split("-")[0]), int(day.split("-")[1]), int(day.split("-")[2])).weekday()
                        dayy = calendar.day_name[dayy]

                        if dayy in count_by_day:
                            count_by_day[dayy] += 1
                        else:
                            count_by_day[dayy] = 1
                        
                        hour = str(time.split(":")[0])
                        if hour in count_by_hours:
                            count_by_hours[hour] += 1
                        else:
                            count_by_hours[hour] = 1


            except:
                print("Error")

    print("--- Show results for user " + user_id + "---\n")
    print("\n--- Message counts\n")

    print("Total " + str(count) + "\n")

    print("In channels: ")
    for a in dict(sorted(count_by_channels.items(), key=lambda item: item[1])):
        print(decode_channel_id(guild_id, a) + "        " + str(count_by_channels[a]))

    print("\nBy day from week: ")
    #for a in dict(sorted(count_by_day.items(), key=lambda item: item[1])):
    for a in count_by_day:
        print(a + "     " + str(round((count_by_day[a] / count * 100))) + " %")
    
    print("\nBy hour:")
    for a in dict(sorted(count_by_hours.items())):
        print(a + "        " + str(count_by_hours[a]))



    print("\n--- Contents\n")

    l = 0
    words = {}

    for f in os.listdir("data/" + guild_id):
        if f == "info":
            continue
        file = open("data/" + guild_id + "/" + f, "r")
        for line in file:
            if line == "":
                continue
            data = base64_decode(line)
            try:
                data = json.loads(data)
                for message in data:
                    if message["author"]["id"] == user_id:
                        content = message["content"]

                        l += len(content)

                        if "/" in content or "@" in content:
                            continue

                        if "<" in content and ">" in content:
                            continue

                        content = content.replace("\n", "")
                        content = content.replace(".", "")
                        content = content.replace("?", "")

                        for a in content.split(" "):
                            if a in words:
                                words[a] += 1
                            else:
                                words[a] = 1
            except:
                print("Error")
    
    print("Message length, median: " + str(round(l / count)))

    print("\nInteressting words:")
    for word in words:
        if words[word] < 5:
            print(word + ", ", end='')

    print("\n")

    for word in words:
        if "isch" in word:
            print(word + ", ", end='')
    
    print("\n")

    for word in words:
        if "$" in word or "€" in word:
            print(word + ", ", end='')

    print("\n\nVery often used\n")

    i = 0
    for word in dict(sorted(words.items(), key=lambda item: item[1])):
        i += 1

        if i > len(words) - 100:
            print(word + ", ", end='')

    print("\n")



guild_id = ""

user_id = ""

activity_user(guild_id, user_id)