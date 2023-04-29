import base64

file = open("download.txt", "r")

c = []

for line in file:
    ch = line.split("#")[2]
    if ch not in c:
        c.append(ch)
        
        print(ch + " - " + base64.b64decode(ch.encode("utf-8")).decode("utf-8"))
