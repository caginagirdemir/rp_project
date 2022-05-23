from flask import Flask,render_template,redirect, jsonify,send_file

from flask_sqlalchemy import SQLAlchemy
import glob
import serial
import os
import random
#import serialGPS

app = Flask(__name__,template_folder="templates")

app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///device.db'
db=SQLAlchemy(app)

class DeviceId(db.Model):
    __tablename__='DeviceId'
    id=db.Column(db.Integer,primary_key=True)
    device_name = db.Column(db.String(15), unique=True, nullable=False)
    device_truck = db.Column(db.String(15), unique=True, nullable=False)



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

@app.route("/gps_test")
def gpstest():
    list_file = os.listdir("/home/pi/Desktop/mywebserver/gps")
    return render_template("gps_test.html",gpsitems=list_file)

@app.route("/livemap")
def maps():
    a1 = read_sensor()
    return render_template("livemap.html",a1=a1)

@app.route('/read_sensor')
def read_sensor():
    # return the actual sensor data here:
    return {'a1': random.random()+39,'a2': random.random()+32}

@app.route('/Ankara/<path:img>')
def get_image(img):
    filename = f'ankara/{img}'
    return send_file(filename, mimetype='image/png')


if __name__=="__main__":
    app.run(port=5000, host='0.0.0.0')
    
    