#!/usr/bin/env python2.7
# Based on:
# demo of "BOTH" bi-directional edge detection
# script by Alex Eames http://RasPi.tv
# http://raspi.tv/?p=6791

# Install:
# sudo apt-get install python-pip
# sudo apt-get install rpi.gpio
# pip install paho-mqtt

import RPi.GPIO as GPIO		
import time
import paho.mqtt.client as mqtt

# ==============================================
# ===== Init GPIO ==============================
# ==============================================
GPIO.setmode(GPIO.BCM)     	# set up BCM GPIO numbering
GPIO.setup(4, GPIO.IN)    	# set GPIO 4 as input (button)

# ==============================================
# ===== Init MQTT client =======================
# ==============================================
mqttc = mqtt.Client("emp_sensor")
mqttc.connect("mqtt_broker_server", 1883)



# ==============================================
# ===== Formatierte Zeitangabe =================
# ==============================================
def get_time():
	return time.strftime("%d.%m.%Y %H:%M:%S")

# ==============================================
# ===== Impuls event verarbeiten ===============
# ==============================================
def handle_impulse():
	print(get_time() + " Impulse detected")
	mqttc.publish("sensor/emp", '{"time": ' + get_time() + '}')

# ==============================================
# ===== Impuls event handler ===================
# ==============================================
def my_callback(channel):
	if GPIO.input(4):     # if port 4 == 1
		print get_time() + " Rising edge detected on 4"
		handle_impulse()
	else:                  # if port 4 != 1
		print get_time() + " Falling edge detected on 4"

		
# when a changing edge is detected on port 4, regardless of whatever 
# else is happening in the program, the function my_callback will be run
GPIO.add_event_detect(4, GPIO.BOTH, callback=my_callback)



# ==============================================
# ===== MAIN ===================================
# ==============================================
try:
	print get_time() + " Starting endless loop ..."
	while True:
		time.sleep(1000)
	
except KeyboardInterrupt:
	print(get_time() + " Keyboard interrupt")
	# GPIO.cleanup()       # clean up GPIO on CTRL+C exit

finally:                   # this block will run no matter how the try block exits
	print("exit()")
	print(get_time() + " cleanup()")
	GPIO.cleanup()         # clean up after yourself