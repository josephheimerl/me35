import time
from motorController import *
import struct
#from dcControl import *
#from roboArm import *


motors = [DCMotor(0), DCMotor(1)]

b = motors[0].resetEncoder(0)
b = motors[1].resetEncoder(0)

motor1 = dcControl(motors[0], 19)
motor2 = dcControl(motors[1], 14)


#motor1.moveDegrees(-5)
#motor2.moveDegrees(-5)


arm = roboArm(2,2,0,0,motor1,motor2)




arm.moveTo(-2,0.1)

time.sleep(3)

for i in range(1,4):
    arm.moveTo(-2,i*0.5)
    
time.sleep(0.5)

for i in range(-4,4):
    arm.moveTo(i*0.5,2)
    
time.sleep(0.5)

for i in range(4,-4,-1):
    arm.moveTo(2,i*0.5)
    
time.sleep(0.5)

for i in range(4,-4,-1):
    arm.moveTo(i*0.5,-2)
    
time.sleep(0.5)

for i in range(-4,-1):
    arm.moveTo(-2,i*0.5)

arm.moveTo(-2,-0.1)

time.sleep(3)

arm.reset()


b = motors[0].resetEncoder(0)
b = motors[1].resetEncoder(0)
