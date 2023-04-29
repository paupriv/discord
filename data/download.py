import requests
import time
import random

dst = "data/"

file = open("download.txt", "r")

for line in file:
    url = line.split("#")[6]

    print("Download.. " + url)

    res = requests.get(url)
    name = ''.join(random.choice("ABCDEFGHIJKLMNOPQRSTUVEXYZ") for i in range(8))
    name += ".mp4"

    save = open(dst + name, "wb")
    save.write(res.content)
    save.flush()
    save.close

    time.sleep(1)