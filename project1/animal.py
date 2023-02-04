import machine
import time
from motorController import *
servos = [Servo(1), Servo(3)]
pushButton = Pin(29, Pin.IN)
sensor = machine.ADC(2)

#
#
#
def readValues():
    lightValue = []
    
    # makes the ears move to signify start or read mode
    earSweep()
    
    # loop to set voltage for 6 discrete motor positions
    dataPoints = 6
    
    # # # # # # # maybe change the 18 to account for data points
    position = range(45, 136, 18)
    
    for i in range(dataPoints):
        # moves motor to current position to be set
        for servo in servos:
            reply = servo.setAngle(position[i])
        
        # wait for button to be pressed to record value
        buttonPressed = pushButton.value()
        while not buttonPressed:
            buttonPressed = pushButton.value()
            time.sleep_ms(1)
        
        time.sleep(0.5)
        
        lightValue.append(sensor.read_u16() * 3.3/(65535))
    
    #moves ears to signify end of read mode
    earSweep()
    return (position, lightValue)

#
# makes ears sweep through posible positions. Used at beginning and end of 
# readValues to signify when the process has begun and ended.
def earSweep():
    for i in range (45, 135):
        for servo in servos:
            reply = servo.setAngle(i)
        time.sleep_ms(5)
    for i in range(135,45,-1):
        for servo in servos:
            reply = servo.setAngle(i)
        time.sleep_ms(5)
        
# 
#
#
def run(position, light):
    reading = sensor.read_u16() * 3.3/(65535)
    
    closestVal = 0
    for i in range(len(light)):
        #check if there is a closer neighbor
        if (abs(light[i]-reading) < abs(light[closestVal]-reading)):
            closestVal = i #save neighbor
    #set angle according to the neighbor
    for servo in servos:
        reply = servo.setAngle(position[closestVal])
    time.sleep_ms(5)



position, lightValue = readValues()

while True:
    buttonPressed = pushButton.value()
    # enter read mode if button is pressed
    if buttonPressed:
        position, lightValue = readValues()
    
    
    run(position, lightValue)

