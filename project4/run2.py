import time
import machine
from motorController import *
from dcControl2 import *
from roboArm2 import *
import json



# defines light pin
light = Pin(29, Pin.OUT)

filein = open("spline.json")

coordinates = json.load(filein)

filein.close()

motors = [DCMotor(0), DCMotor(1)]
joints = dcControl2(motors, [25,20])
arm = roboArm2(2,2,joints)

nPoints = len(coordinates[1])

# move to starting position
arm.moveTo(0.158,0.158, [1,1],1000)
time.sleep_ms(500)

light.value(1)
# loop through coordinates supplied by json
for i in range(1, nPoints):
    x = float(coordinates[0][i])
    y = float(coordinates[1][i])
    arm.moveTo(x,y,[2,1],30)
light.value(0)

# wait for a bit and then reset the arm
time.sleep_ms(500)
arm.reset()
