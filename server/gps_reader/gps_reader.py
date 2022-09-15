import serial
import sqlite3
import time as t
import mmap
import random

filepath='/home/pi/Desktop/server/variables.txt'

file_object=open(filepath,mode="r+",encoding="utf8")
mmap_object=mmap.mmap(file_object.fileno(),0,access=mmap.ACCESS_WRITE,offset=0)


#/dev/ttyACM0

time=""
lat=0
long=0
h=0
nsatellites=0
height=0
Vprecision=0

def getSerialAvailable(port):
    
    try:
        return serial.Serial(port, baudrate = 38400, timeout = 5)
    except:
        return "none"



while True:
    
    try:
        
        port='/dev/ttyACM0'
        ser=getSerialAvailable(port)
        if ser=="none":
            t.sleep(1)
            print("Serial Port Not Available")
        else:
            def insert_f(data_t):
                con=sqlite3.connect('vehicle.db')
                cursor=con.cursor()
                insert_sql="""INSERT INTO gpsdata(t,lat,long,h,sat_n) VALUES (?,?,?,?,?);"""
                cursor.execute(insert_sql,data_tuple)
                con.commit()
                cursor.close()
                con.close() 
            
            def decode(coord):
                #Converts DDDMM.MMMMM > DD deg MM.MMMMM min
                x = coord.split(".")
                head = x[0]
                tail = x[1]
                deg = float(head[0:-2])
                mins = float(head[-2:]+'.'+tail)/60
                return deg + mins

            while True:
                
                data = ser.readline()
                #print(data)
                #print("**************************** line /n")

                
                if str(data[0:6]) == "b'$GNGGA'":
                    #print("check point 1")
                     sdata = str(data).split(",")
                     if sdata[2] == "":
                         print("no satellite data available")
                     else:
                         print('******************line \n')
                         
                         hour=int(sdata[1][0:2])+3
                         time = str(hour) + ":" + sdata[1][2:4] + ":" + sdata[1][4:6]
                         print(str(time))
                         #time=str(hour)
                         
                         #rand_number=random.randint(10,50)
                         #rand_number="bb"
                         mmap_object.seek(0) #rewind geri sarma
                         
                         
                         mmap_object.write(bytes(str(time),encoding="utf8"))
                         
                         lat = decode(sdata[2]) #latitude
                         #print(str(lat)+'\n')
                         lat=float(str(lat))
                         lat=format(lat,'.6f')
                         print(str(lat)+'\n')
                         mmap_object.write(bytes(str(lat),encoding="utf8"))
                         
                         
                         
                         long = decode(sdata[4]) #latitude
                         #print(str(long)+'\n')
                         long=float(str(long)[0:9])
                         long=format(long,'.6f')
                         print(str(long)+'\n')
                         mmap_object.write(bytes(str(long),encoding="utf8"))
                         
                         
                         nsatellites = sdata[7] #latitude
                         print(str(nsatellites)+'\n')
                         Vprecision = sdata[8] #latitude
                         print(str(Vprecision)+'\n')
                         height = sdata[9] #latitude
                         print(str(height)+'\n')
                         data_tuple=(time,lat,long,height,nsatellites)
                         insert_f(data_tuple)
                     


    except KeyboardInterrupt:
        print("____Aborted")
        ser.close()
        break
        #file2.close()
        
    
 
