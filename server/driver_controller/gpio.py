import RPi.GPIO as GPIO
from time import sleep
import mmap

filepath='/home/pi/Desktop/server/variables.txt'

file_object=open(filepath,mode="r+",encoding="utf8")
mmap_object=mmap.mmap(file_object.fileno(),0,access=mmap.ACCESS_WRITE,offset=0)


GPIO.setmode(GPIO.BCM)
GPIO.setup(27, GPIO.IN)
while True:
    if(GPIO.input(27)==1):
        mmap_object.seek(78)
        mmap_object.write(bytes(str(GPIO.input(27)),encoding="utf8"))
        if(mmap_object[79:80].decode()=='0'):
            mmap_object.seek(79)
            mmap_object.write(bytes(str(1),encoding="utf8"))
        print(GPIO.input(27))
        sleep(1)
    else:
        mmap_object.seek(78)
        mmap_object.write(bytes(str(0),encoding="utf8"))
        mmap_object.write(bytes(str(0),encoding="utf8"))
        mmap_object.write(bytes(str(0),encoding="utf8"))
        print(GPIO.input(27))
        sleep(1)
# while True:
#     if GPIO.input(27) == 1:
#         print("button pressed")
#         sleep(1)
#     elif GPIO.input(27) == 0:
#         print("button not pressed")
#         sleep(1)