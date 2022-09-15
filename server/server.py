from flask import Flask,render_template,redirect, jsonify,send_file
import glob
import serial
import os
import random
import mmap


filepath='/home/pi/Desktop/server/variables.txt'
filepath_driver_word='/home/pi/Desktop/server/driver_word.txt'


file_object=open(filepath,mode="r",encoding="utf8")
mmap_object=mmap.mmap(file_object.fileno(),length=0,access=mmap.ACCESS_READ,offset=0)

app = Flask(__name__,template_folder="templates")


@app.route("/")
def hello():
    return render_template("index.html")

@app.route("/ports")
def port():
    ports=glob.glob('/dev/tty[A-Za-z]*')
    return render_template("ports.html",items=ports)

#@app.route("/readgps")
#def readgps():
#    serialGPS.readGPS()
#     if serialGPS.readGPS()==0:
#         return render_template("error.html")
#     else:
#         return redirect(url_for("hello"))
# 
# @app.route("/gps_test")
# def gpstest():
#     list_file = os.listdir("/home/pi/Desktop/mywebserver/gps")
#     return render_template("gps_test.html",gpsitems=list_file)
# 
@app.route("/livemap")
def maps():
    a1 = read_sensor()
    return render_template("livemap.html",a1=a1)

@app.route('/read_sensor')
def read_sensor():
    #get variables from RAM
    mmap_object.seek(0)
    #data = {'time': mmap_object[0:1] ,'lat': gps_reader.lat,'long': gps_reader.long,'h': gps_reader.h,'sat_n': gps_reader.nsatellites}
    
    
    data = {'hour': mmap_object[0:2],
            'min':mmap_object[3:5],
            'sec':mmap_object[6:8],
            'lat':float(mmap_object[8:17]),
            'long':float(mmap_object[17:26]),
            'driver_name':mmap_object[27:58],
            'driver_key_state':mmap_object[78:79],
            'driver_card_state':mmap_object[79:80],
            'driver_face_recognation_state':mmap_object[80:81],
            'shift_start_date':mmap_object[60:68],
            'shift_start_time':mmap_object[69:77]
            }
    return jsonify(data)


@app.route("/sensorpage")
def sensors():
    #a1 = read_sensor()
    return render_template("sensorpage.html")#,a1=a1


@app.route('/mapfile/<path:img>')
def get_image(img):
    filename = f'mapfile/{img}'
    return send_file(filename, mimetype='image/png')


if __name__=="__main__":
    app.run(port=5000, host='0.0.0.0')
    
    