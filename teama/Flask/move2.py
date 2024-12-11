from PCA9685 import PCA9685
import time
import moteur 
import numpy as np

Motor = moteur.MotorDriver()

def move(speed,angle):
    '''
    speed entre 0 et 1
    angle entre -pi et pi
    '''
    angle=angle/np.pi
    left=max(min(2-np.abs(4*angle+1),1),-1)
    right=max(min(2-np.abs(4*angle-1),1),-1)
    
    fr='forward'
    fl='forward'
    if left<0:
        fl='backward'
    if right<0:
        fr='backward'   

    Motor.MotorRun(0,fl, speed*np.abs(left)*100)
    Motor.MotorRun(1,fr, speed*np.abs(right)*100)

        
