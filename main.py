from ubinascii import hexlify
import machine
from umqttsimple import MQTTClient
import utime

# MQTT Stuff
CLIENT_ID = hexlify(machine.unique_id()) #To create an MQTT client, we need to get the PICOW unique ID
MQTT_BROKER = "io.adafruit.com" # MQTT broker IP address or DNS
PORT = 1883
ADAFRUIT_USERNAME = "michelow"
ADAFRUIT_PASSWORD = "aio_xnAU80fke1w7PYPBzSyxLnQZYAwO"
SUBSCRIBE_TOPIC = b"michelow/f/gate"

#print(f"Begin connection with MQTT Broker :: {MQTT_BROKER}")
mqttClient = MQTTClient(CLIENT_ID, MQTT_BROKER, PORT, ADAFRUIT_USERNAME, ADAFRUIT_PASSWORD, keepalive=60)
mqttClient.connect()
#print(f"Connected to MQTT  Broker :: {MQTT_BROKER} successfully!")

# pins
led_onboard = machine.Pin("LED", machine.Pin.OUT)

# MQTT subscribe callback (gate info)    
def sub_cb(topic, msg):
    if msg.decode() == "true":
        led_onboard.value(1)
    else:
        led_onboard.value(0)

mqttClient.set_callback(sub_cb) # whenever a new message comes (to picoW), print the topic and message (The call back function will run whenever a message is published on a topic that the PicoW is subscribed to.)
mqttClient.connect()
mqttClient.subscribe(SUBSCRIBE_TOPIC)

while True:
    mqttClient.check_msg()
    utime.sleep_ms(500)