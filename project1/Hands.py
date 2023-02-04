import time
from motorController import *

board = NanoMotorBoard()
print("reboot")
board.reboot()
time.sleep_ms(500)

servos = [Servo(0), Servo(1)]
   
 while True:
     for i in range(60,150):
         for servo in servos:
             reply = servo.setAngle(i)
         time.sleep_ms(5)
     for i in range(150,60,-1):
         for servo in servos:
             reply = servo.setAngle(i)
         time.sleep_ms(5)
