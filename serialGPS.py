import time
import pynmea2
import serial

# def readGPS():

ser = serial.Serial('/dev/ttyACM0', 38400, timeout=5.0)
file2 = open("gps/MyFile2.csv","w+")
file2.write('hour,minute,second,latitude,longitude\n')
try:
    while 1:
        newdata=ser.readline()
        #print(newdata[0:6])
        #print("-----------test /n")
        
        
        if str(newdata[0:6])=="b'$GNGGA'":
            word=str(newdata[6:]).split(',')
            
            print(word)
            
            time=str(word[1])
#             if time=="":
#                 print("0")
#                 #return 0
#                 time=0
#             else:
            time=time[:-3]
            hour=time[0:2]
            minute=time[2:4]
            second=time[4:6]
            
            latitude=str(word[2])
#             if latitude=="":
#                 print("0")
#                 #return 0
#                 latitude=0
#             else:
            dot = latitude.find('.')
            temp_value_hour=int(latitude[:dot-2])
            temp_value_min=float(latitude[dot-2:])/60
            temp_value_min=str(temp_value_min)
            latitude=str(temp_value_hour)+'.'+temp_value_min[2:]
                         
                         
            longitude=str(word[4])
#             if longitude=="":
#                 print("0")
#                 #return 0
#                 longitude=0
#             else:
            dot = longitude.find('.')
            temp_value_hour=int(longitude[:dot-2])
            temp_value_min=float(longitude[dot-2:])/60
            temp_value_min=str(temp_value_min)
            longitude=str(temp_value_hour)+'.'+temp_value_min[2:]
            file2.write(hour+','+minute+','+second+','+latitude+','+longitude+'\n')
except KeyboardInterrupt:
    print("____Aborted")
    ser.close()
    file2.close()
