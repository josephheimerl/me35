import time
from motorController import *
import struct

class dcControl():
    
    def __init__(self, motor, duty):
        self.motor = motor
        self.duty = duty
        b = self.motor.setDuty(0)
        b = self.motor.resetEncoder(0)
        
        #encoder per degree
        self.epd = 1180/360
        
    def setAngle(self, angle):
        
        currCount = self.motor.readEncoder()
        
        goalCount = angle*self.epd
        
        direction = 0
        if goalCount > currCount:
            direction = 1
        else:
            direction = -1
        
        self.motor.setDuty(self.duty*direction)
        
        currCount = self.motor.readEncoder()
        
        while (direction*(goalCount-currCount))>0:
            currCount = self.motor.readEncoder()
            time.sleep_ms(1)
         
        #print("")
        #print("setAngle Counts:")
        #print(goalCount)
        #print(currCount)
        #print(self.motor.readEncoder())
        #print("")
         
        self.motor.setDuty(0)
         
    def moveDegrees(self, angle):
         
        initalCount = self.motor.readEncoder()
        
        #print(initialCount)
        
        goalCount = angle*self.epd
        
        if goalCount > 0:
            direction = 1
        else:
            direction = -1
        
        b = self.motor.setDuty(self.duty*direction)
        
        #encoder count for this function based on initial encoder position
        currCount = self.motor.readEncoder() - initalCount
        
        while (direction*(goalCount-currCount)) > 0:
            currCount = self.motor.readEncoder() - initalCount
        
        time.sleep_ms(1)
        
        self.motor.setDuty(0)
        
        #time.sleep(0.25)
        #print("")
        #print(goalCount)
        #print(currCount)
        #print(self.motor.readEncoder())
        #print("")
     
    def reset(self):
        self.motor.setDuty(0)
        self.motor.resetEncoder(0)