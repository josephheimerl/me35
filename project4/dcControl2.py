import time
from motorController import *
import struct

class dcControl2():
    # constructor arguments:
    #    motors: array of DCMotor objects to be controlled by the class
    #    dutyMax: array of maximum duty cycle to be allowed for each motor. 
    #             Length must match motors.
    def __init__(self, motors, dutyMax):
        self.motors = motors
        self.dutyMax = dutyMax
        for motor in self.motors:
            b = motor.setDuty(0)
            b = motor.resetEncoder(0)

            #encoder per degree
            self.epd = 1180/360
    
    # setAngles arguments:
    #    angles: array of desired angles for each motor to move to. Length must match
    #            amount of motors being used by the class.
    #    Kp: array of desired proportional control constants for each motor. Length 
    #        must match amount of motors being used by the class.
    #    moveTime: time alloted to the motors to move to the input angles in ms
    def setAngles(self, angles, Kp, moveTime):
        
        if len(angles) != len(self.motors):
            print("setAngles: angles list size must match motors")
            return
        
        if len(Kp) != len(self.motors):
            print("setAngles: Kp list size must match motors")
            return
        
        goalCounts = []
        errors = []
        i = 0
        for motor in self.motors:
            goalCounts.append(angles[i]*self.epd)
            errors.append(goalCounts[i] - motor.readEncoder())
            i += 1

        power = []
        i = 0
        for motor in self.motors:
            power.append(int(Kp[i]*(errors[i])))
            power[i] = max(-1*self.dutyMax[i], (min(power[i], self.dutyMax[i])))
            motor.setDuty(power[i])
            i += 1
        
        initialTime = time.ticks_ms()
        while initialTime + moveTime > time.ticks_ms():
            i = 0
            for motor in self.motors:
                errors[i] = goalCounts[i] - motor.readEncoder()
                power[i] = int(Kp[i]*(errors[i]))
                power[i] = max(-1*self.dutyMax[i], (min(power[i], self.dutyMax[i])))
                motor.setDuty(power[i])
                i += 1
        
        for motor in self.motors:
            motor.setDuty(0)
            
