from evdev import InputDevice, categorize, ecodes
import numpy
import mmap
import sqlite3
import time

driver_rfid=numpy.arange(10)

filepath='/home/pi/Desktop/server/variables.txt'

file_object=open(filepath,mode="r+",encoding="utf8")
mmap_object=mmap.mmap(file_object.fileno(),0,access=mmap.ACCESS_WRITE,offset=0)



i=0
p=0

device=InputDevice("/dev/input/event0") #rfid reader
while True:
    time.sleep(0.75)
    for event in device.read_loop():
        if(mmap_object[78:79].decode()=='1' and mmap_object[79:80].decode()=='1'):
            if event.type == ecodes.EV_KEY:
                data=categorize(event)
                
#                 if(flag_2==1 and data.keycode[-1]=='R'):
#                     print("check")
#                     flag=1
                
                if(data.keycode[-1]!='R' and i%2!=0):        
                    driver_rfid[p]=data.keycode[-1]
                    i=i+1
                    p=p+1
                elif(data.keycode[-1]!='R'):
                    i=i+1
                elif(data.keycode[-1]=='R'):  # and flag==0
                    #print(driver_rfid[:])
                    driver_id='%d%d%d%d%d%d%d%d%d%d' % (driver_rfid[0],driver_rfid[1],driver_rfid[2],driver_rfid[3],driver_rfid[4],driver_rfid[5],driver_rfid[6],driver_rfid[7],driver_rfid[8],driver_rfid[9])
                    print(driver_id)

                    ###db side
                    con=sqlite3.connect('driver.db')
                    cursor=con.cursor()    
                    sql_query="select * from drivers where driver_id="+"'"+driver_id+"'"+";"      
                    cursor.execute(sql_query)
                    rows=cursor.fetchall()
                    cursor.close()
                    con.close()
                    
                    mmap_object.seek(27)
                    driver_fullname=[" " for x in range(0,30)]
                    driver_fullname[29]="\n"
                    
                    #db den gelen ismi değişkene dolduruyor
                    for i in range(0,len(rows[0][2])):
                        driver_fullname[i]=rows[0][2][i]
                        #print(mmap_object.tell())
                    
                    #RAM e yazıyor
                    for i in range(0,len(driver_fullname)-1):
                        mmap_object.write(bytes(str(driver_fullname[i]),encoding="utf8"))
                        #print(mmap_object.tell())
                    
                    mmap_object.seek(79)
 
                    mmap_object.write(bytes(str(2),encoding="utf8"))
                    mmap_object.write(bytes(str(1),encoding="utf8"))

                    mmap_object.seek(85)
                    mmap_object.write(bytes(str(driver_id),encoding="utf8"))

                    p=0
                    i=0                    
                    
                    
                    
                    
                    
                    
                    

