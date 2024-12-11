import os
from flask import Flask, render_template, request
from PCA9685 import PCA9685
import time
import moteur 
import camera

Motor = moteur.MotorDriver()

app=Flask(__name__)

@app.route('/') 
@app.route("/home")
def home():
    return render_template("site.html")

@app.route('/get_carspeed', methods=['POST'])
def get_carspeed():
    global carSpeed
    data=request.get_json()
    carSpeed = float(data.get('carSpeed'))
    return ""

@app.route('/bouton_down', methods=['POST'])
def DOWN():
    print("DOWN")
    print(type(carSpeed),carSpeed)
    Motor.MotorRun(0, 'backward', carSpeed)
    Motor.MotorRun(1, 'backward', carSpeed)
    return ""

@app.route('/bouton_right', methods=['POST'])
def RIGHT():
    print("RIGHT")
    print(carSpeed)
    Motor.MotorRun(0, 'forward', carSpeed)
    Motor.MotorRun(1, 'forward', 0.5*carSpeed)
    return ""

@app.route('/bouton_up', methods=['POST'])
def UP():
    print("UP")
    print(carSpeed)
    Motor.MotorRun(0, 'forward', carSpeed)
    Motor.MotorRun(1, 'forward', carSpeed)

@app.route('/bouton_left', methods=['POST'])
def LEFT():
    print("LEFT")
    print(carSpeed)
    Motor.MotorRun(0, 'forward', 0.5*carSpeed)
    Motor.MotorRun(1, 'forward', carSpeed)
    return ""

@app.route('/bouton_stop', methods=['POST'])
def STOP():
    print("Stop")
    Motor.MotorRun(0, 'forward', 0)
    Motor.MotorRun(1, 'forward', 0)
    return ""

if __name__ == '__main__':
    from waitress import serve
    serve(app, host="0.0.0.0", port=8080)

