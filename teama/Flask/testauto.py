import camera
import time
import moteur

Motor = moteur.MotorDriver()

#première rotation pour mettre le robot parallèle au qr code
liste=camera.findAruco()

while liste==None:
    liste=camera.findAruco()
    print(liste)
    print('ROTATION')
    Motor.MotorRun(0, 'forward', 20)
    Motor.MotorRun(1, 'backward', 20)
    time.sleep(1)
    Motor.MotorRun(0, 'forward', 0)
    Motor.MotorRun(1, 'forward', 0)
    time.sleep(3)


#rotation de Phi - 90°
Motor.MotorRun(0,'forward',20)
Motor.MotorRun(1, 'backward', 20)

time.sleep((90-liste[1])/413) #omega represente la vitesse de rotation du robot avec 100% backwards et forward, on le mesure experimentalement avec 100% de batterie

Motor.MotorRun(0,'forward',0)
Motor.MotorRun(1,'forward',0)

#robot avance et fait des rotations 90° jusqu'a atteindre le cône d'acceptance
while abs(liste[2]) > 50 :
    Motor.MotorRun(0,'forward',100)
    Motor.MotorRun(1,'forward',100)
    time.sleep(1)
    Motor.MotorRun(0, 'backward', 100)
    Motor.MotorRun(1, 'forward', 100)
    time.sleep(90/413)
    Motor.MotorRun(0, 'backward', 0)
    Motor.MotorRun(1, 'backward', 0)

while liste[0]>0.2:
    Motor.MotorRun(0,'forward',100)
    Motor.MotorRun(1,'forward',100)







print(liste)
while True :
    while liste==None:
        liste=camera.findAruco()
        print(liste)
        print('ROTATION')
        Motor.MotorRun(0, 'forward', 25)
        Motor.MotorRun(1, 'backward', 25)
        time.sleep(1)
        Motor.MotorRun(0, 'forward', 0)
        Motor.MotorRun(0, 'forward', 0)

    while liste!=None :
    #rotation de Phi - 90°
        liste=camera.findAruco()
        Motor.MotorRun(0,'forward',25)
        Motor.MotorRun(1, 'backward', 25)

        time.sleep(abs(90-liste[1])/413) #omega represente la vitesse de rotation du robot avec 100% backwards et forward, on le mesure experimentalement a>
        Motor.MotorRun(0,'forward',0)
        Motor.MotorRun(1,'forward',0)

    #robot avance et fait des rotations 90° jusqu'a atteindre le cône d'acceptance
        while abs(liste[2]) < 50:
            Motor.MotorRun(0,'forward',25)
            Motor.MotorRun(1,'forward',25)
            time.sleep(1)
            if liste[2]<0 :
                Motor.MotorRun(0, 'backward', 25)
                Motor.MotorRun(1, 'forward', 25)
                time.sleep(90/413)
                Motor.MotorRun(0, 'backward', 0)
                Motor.MotorRun(1, 'backward', 0)
                liste=camera.findAruco()
                time.sleep(1)
                if abs(liste[2]) < 50 :
                    break
                Motor.MotorRun(1, 'backward', 25)
                Motor.MotorRun(0, 'forward', 25)
                time.sleep(90/413)
                Motor.MotorRun(0, 'backward', 0)
                Motor.MotorRun(1, 'backward', 0)
            elif liste[2]>0  :
                Motor.MotorRun(1, 'backward', 25)
                Motor.MotorRun(0, 'forward', 25)
                time.sleep(90/413)
                Motor.MotorRun(0, 'backward', 0)
                Motor.MotorRun(1, 'backward', 0)
                liste=camera.findAruco()
                time.sleep(1)
                if abs(liste[2]) < 50 :
                    break
                Motor.MotorRun(0, 'backward', 25)
                Motor.MotorRun(1, 'forward', 25)
                time.sleep(90/413)
                Motor.MotorRun(0, 'backward', 0)
                Motor.MotorRun(1, 'backward', 0)


        while liste[0]>0.2 :
            Motor.MotorRun(0,'forward',25)
            Motor.MotorRun(1,'forward',25)
