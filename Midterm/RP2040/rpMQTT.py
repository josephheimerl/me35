import machine
import mqtt_CBR
import time
from secrets import TuftsWireless as wifi

# allows us to blink led connected to D2 for debugging
led = machine.Pin(25, machine.Pin.OUT)
def blink(delay = 0.1):
    led.on()
    time.sleep(delay)
    led.off()

# callback function, not used as of now
def whenCalled(topic, msg):
    print((topic.decode(), msg.decode()))

class rpMQTT():
    def __init__(self, mqtt_broker, wifiInfo = wifi, topic_pub = 'angles', client_id = "Joseph's rp2040"):
        mqtt_CBR.connect_wifi(wifiInfo)
        self.mosq_server = mqtt_CBR.mqtt_client(client_id, mqtt_broker, whenCalled)
        self.topic_pub = topic_pub
        
        blink()
        time.sleep(0.1)
        blink()
        time.sleep(0.1)
        blink(1)
    
    def pub(self,msg):
        try:
            self.mosq_server.publish(self.topic_pub, msg)
            blink()
        except OSError as e:
            print(e)
            self.mosq_server.connect()
    def disconnect(self):
        self.mosq_server.disconnect()
        
        blink(1)
        time.sleep(0.1)
        blink()
        time.sleep(0.1)
        blink()
        time.sleep(0.1)
        blink()
        
        