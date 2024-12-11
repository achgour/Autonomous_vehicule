#ce programme permet de tester la vitesse de rotation du robot 

import moteur 
import time
'''
Motor=moteur.MotorDriver()
Motor.MotorRun(0, 'backward', 100)
Motor.MotorRun(1, 'forward', 100)
time.sleep(5)
Motor.MotorRun(0, 'backward', 0)
Motor.MotorRun(1, 'backward', 0)'''

#test rotation 90° à vitesse 100%

Motor=moteur.MotorDriver()
Motor.MotorRun(0, 'backward', 100)
Motor.MotorRun(1, 'forward', 100)
time.sleep(90/413)
Motor.MotorRun(0, 'backward', 0)
Motor.MotorRun(1, 'backward', 0)
