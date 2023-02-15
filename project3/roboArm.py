import time
from motorController import *
#from dcControl import *
import struct
import math


class roboArm():
    
    #constructor arguments:
    #    l1: length of "upper arm"
    #    l2: length of "forearm"
    #    t1i: initial angle of shoulder, in degrees,
    #         relative to desired angle of 0
    #    t2i: initial angle of elbow, relative to collinearity
    #         or forearm and upper arm(fully extended)
    #    shoulder: dcControl object corresponding to shoulder motor
    #    elbow: dcControl object corresponding to elbow motor
    
    def __init__(self, l1, l2, t1i, t2i, shoulder, elbow):
        self.l1 = l1
        self.l2 = l2
        self.shoulder = shoulder
        self.elbow = elbow
        
        self.elbow.moveDegrees(-t2i)
        self.elbow.reset()
        
        self.shoulder.moveDegrees(-t1i)
        self.shoulder.reset()
    
    def moveTo(self, x, y): 
        l3 = math.sqrt(x**2+y**2)
        if l3 > (self.l1 + self.l2):
            print("Error: target position out of range")
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
        
        #print("")
        #print("target angles:")
        #print(t1)
        #print(t2)
        #print("")
        
        self.shoulder.setAngle(t1)
        self.elbow.setAngle(t2)

    def reset(self):
        self.shoulder.setAngle(0)
        self.elbow.setAngle(0)
        self.shoulder.reset()
        self.elbow.reset()


