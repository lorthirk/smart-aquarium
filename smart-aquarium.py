#!/usr/bin/python3

from pubnub import Pubnub
from w1thermsensor import W1ThermSensor
import time
from RPLCD import CharLCD
from os.path import dirname, abspath

# init temperature probe library
sensor = W1ThermSensor()
# init Pubnum keys
keys_file = dirname(abspath(__file__)) + "/conf/pubnub.keys"
keys = {}
# Pubnub channel
channel = "smart-aquarium"
# Reading interval in seconds
sleep_interval = 5
''' 
init LCD. Pinout configuration based on 
https://cdn-learn.adafruit.com/downloads/pdf/drive-a-16x2-lcd-directly-with-a-raspberry-pi.pdf
'''
lcd = CharLCD(cols=16, rows=2, pin_rs=22, pin_rw=None, pin_e=18, pins_data=[16, 11, 40, 15])
# Read Pubnub's keys from conf/pubnub.keys
with open(keys_file) as f:
    for line in f:
        name, var = line.partition("=")[::2]
        keys[name.strip()] = var.strip()

print(keys)
pubnub = Pubnub(keys["pub"], keys["sub"])

# Various callbacks definition
def callback(message, channel):
    print(message)
  
def error(message):
    print("ERROR : " + str(message))
  
def connect(message):
    print("CONNECTED")
    print(pubnub.publish(channel=channel, message='Hello from the PubNub Python SDK'))
  
def reconnect(message):
    print("RECONNECTED")
  
def disconnect(message):
    print("DISCONNECTED")

# Read every N seconds and publish to Pubnub
while (True):
    temperature = {}
    temp_value = sensor.get_temperature()
    temp_date_pubnub = time.strftime("%Y-%m-%d %H:%M:%S")
    temp_date_lcd = time.strftime("%Y-%m-%d %H:%M")
    temperature["value"] = temp_value
    temperature["date"] = temp_date_pubnub
    pubnub.publish(channel, temperature, error=error)
    lcd.write_string("Temp: " + str(temp_value) +  "\r\n" + temp_date_lcd)
    time.sleep(sleep_interval)
