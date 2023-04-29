

size = 0

file = open("download.txt", "r")

for line in file.readlines():
    size += int(line.split("#")[5])

print(str(round(size)) + " B")
print(str(round(size / 1024)) + " KB")
print(str(round(size / 1024 / 1024)) + " MB")
print(str(round(size / 1024 / 1024 / 1024)) + " GB")
