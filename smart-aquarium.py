from pubnub import Pubnub
from w1thermsensor import W1ThermSensor
import time
from datetime import datetime

# init temperature probe library
sensor = W1ThermSensor()
# init Pubnum keys
keys_file = "conf/pubnub.keys"
keys = {}
# Pubnub channel
channel = "smart-aquarium"
# Reading interval in seconds
sleep_interval = 5

# Read Pubnub's keys from conf/pubnub.keys
with open(keys_file) as f:
    for line in f:
        name, var = line.partition("=")[::2]
        keys[name.strip()] = var

pubnub = Pubnub(keys["pub"], keys["sub"])

# Various callbacks definition
def callback(message, channel):
    print(message)
  
def error(message):
    print("ERROR : " + str(message))
  
def connect(message):
    print("CONNECTED")
    print(pubnub.publish(channel='my_channel', message='Hello from the PubNub Python SDK'))
  
def reconnect(message):
    print("RECONNECTED")
  
def disconnect(message):
    print("DISCONNECTED")

# Read every N seconds and publish to Pubnub
while (True):
    temperature = {}
    temperature["value"] = sensor.get_temperature()
    temperature["date"] = datetime.now().date().isoformat()
    pubnub.publish(channel, temperature, error=error)
    time.sleep(sleep_interval)
