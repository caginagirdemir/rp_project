import smbus
import time

bus=smbus.SMBus(1)
address=0x48
#def read(control):
    #write_address=bus.write_byte(address,control,0)


while True:
    bus.write_byte(address,0x40)
    value=bus.read_byte(address)
    print(value)
    time.sleep(0.1)
#     poti=read(0x40)
#     light=read(0x41)
#     temp=read(0x42)
#     ain2=read(0x43)
#     print("tempature:", temp, "light:",light, "Voltage-Poti:",poti)
#     time.sleep(1)