import os

#print(os.listdir("/home/pi/Desktop/mywebserver/gpstest"))
for file in os.listdir("/home/pi/Desktop/mywebserver/gpstest"):
    if file.endswith(".csv"):
        print(os.path.join("/gpstest"),file)