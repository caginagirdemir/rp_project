import io
import pynmea2
import serial
import time

ser=serial.Serial()
ser.port='/dev/ttyACM0'
ser.baudrate=34800
ser.timeout=5.0
sio=io.TextIOWrapper(io.BufferedRWPair(ser, ser))
ser.open()
try:
    while(True):
        try:
            line=sio.readline()
            print(line)
            print("||||||||||| /n")
        except serial.SerialException as e:
            print('Device error:{}'.format(e))
            break
        except pynmea2.ParseError as e:
            print('Parse error:{}'.format(e))
            continue
        
except KeyboardInterrupt:
    print("___Aborted")
    ser.close()
