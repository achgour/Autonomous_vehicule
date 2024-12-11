import camera
import time
import moteur

Motor = moteur.MotorDriver()



Motor.MotorRun(0,'forward',100)
Motor.MotorRun(1,'forward',100)
time.sleep(1.5)
Motor.MotorRun(0,'forward',0)
Motor.MotorRun(1,'forward',0)
time.sleep(3)


Motor.MotorRun(0, 'backward', 100)
Motor.MotorRun(1, 'forward', 100)
time.sleep(50/413)

Motor.MotorRun(0,'forward',50)
Motor.MotorRun(1,'forward',50)
time.sleep(5)
Motor.MotorRun(0,'forward',0)
Motor.MotorRun(1,'forward',0)
time.sleep(1)

liste=camera.findAruco()
if liste[4]%2==0 :
    Motor.MotorRun(0, 'backward', 100)
    Motor.MotorRun(1, 'forward', 100)
    time.sleep(180/413)
    Motor.MotorRun(0, 'forward', 100)
    Motor.MotorRun(1, 'forward', 100)
    time.sleep(4)
    Motor.MotorRun(0, 'backward', 100)
    Motor.MotorRun(1, 'forward', 100)
    time.sleep(180/413)
    Motor.MotorRun(0, 'forward', 100)
    Motor.MotorRun(1, 'forward', 100)
    time.sleep(4)

elif liste[4]%2!=0 : 
    Motor.MotorRun(0, 'forward', 100)
    Motor.MotorRun(1, 'forward', 100)
    time.sleep(1)
    Motor.MotorRun(0, 'backward', 100)
    Motor.MotorRun(1, 'forward', 100)
    time.sleep(180/413)
    Motor.MotorRun(0, 'forward', 100)
    Motor.MotorRun(1, 'forward', 100)
    time.sleep(4)




    




