import time
from motorController import *
from dcControl2 import *
import struct
import math


class roboArm2():
    
    #constructor arguments:
    #    l1: length of "upper arm"
    #    l2: length of "forearm"
    #    motors: dcControl2 object corresponding to shoulder and elbow motors
    
    def __init__(self, l1, l2, motors):
        self.l1 = l1
        self.l2 = l2
        self.arm = motors
        
    #moveTo arguments:
    #    x: desired x coordinate
    #    y: desired y coordinate
    #    Kp: list of 2 desired proportional control constants. First value corresponds
    #        to the shoulder motor, second to the elbow.
    #    moveTime: time alloted to the arm to move to the input coordinates in ms
    def moveTo(self, x, y, Kp, moveTime): 

        l3 = math.sqrt(x**2+y**2)
        if l3 > (self.l1 + self.l2):
            print("Error: target position out of range")
            return
        
        # handles case of going to origin
        if l3 == 0:
            self.arm.setAngles([0,180], Kp, moveTime)
            return
        
        b1 = (self.l1**2 + l3**2 - self.l2**2)/(2*self.l1*l3);
        a1 = math.atan2(math.sqrt(1-b1**2),b1);
    
        t1 = math.atan2(y,x) - a1
    
        
        b2 = (self.l1**2 + self.l2**2 - l3**2)/(2*self.l1*self.l2);
        a2 = math.atan2(math.sqrt(1-b2**2),b2);
    
        t2 = math.pi - a2
        
        # convert to radians
        t1 = t1 * 180/math.pi
        t2 = t2 * 180/math.pi
        

        self.arm.setAngles([t1,t2], Kp, moveTime)

    def reset(self):
        self.arm.setAngles([0,0],[1,1],1000)


