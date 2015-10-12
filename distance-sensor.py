#!/usr/bin/python

# distance measurement with the hc-sr04 distance sensor taken and adapted form the modmypi tutorial below 
# http://www.modmypi.com/blog/hc-sr04-ultrasonic-range-sensor-on-the-raspberry-pi

import RPi.GPIO as GPIO
import json
import sys
import time
from time import localtime
import datetime


FREQUENCY_SECONDS      = 5 # How long to wait (in seconds) between measurements.
TEXTFILE = 'filename.txt' # your .txt file

GPIO.setmode(GPIO.BCM)

# pins thge pi uses to communicate with the distance sensor
TRIG = 23
ECHO = 24

print 'Logging sensor measurements to {0} every {1} seconds.'.format(TEXTFILE, FREQUENCY_SECONDS)
print 'Press Ctrl-C to quit.'

def distance(): # a detailed description of how this function works is available in the modmypi tutorial
	GPIO.setup(TRIG,GPIO.OUT)
	GPIO.setup(ECHO,GPIO.IN)
	 
	GPIO.output(TRIG, False)
	time.sleep(2)
	
	GPIO.output(TRIG, True)
	time.sleep(0.00001)
	GPIO.output(TRIG, False)
	 
	while GPIO.input(ECHO)==0:
	  pulse_start = time.time()
	 
	while GPIO.input(ECHO)==1:
	  pulse_end = time.time()
	 
	pulse_duration = pulse_end - pulse_start 
	distance = pulse_duration * 17150
	distance = distance * 0.39370
	distance = round(distance, 2)
		 
	return distance

	GPIO.cleanup()

def logMedian():
	try:
		data = [] # array of measurements
		loop = 0
		print 'beginning measurements'

		while loop < 9:
			m = distance() # calls the function to measure distance
			data.append(m) # appends the measurement to data[]
			loop = loop + 1

		data.sort() # organizes data[] by amount
		median = data[4]  # the median of the measurements
		print ('you are {0} inches from robo pope').format(median)

		# the median measuremt and time are then written to your .txt file
		data = str(median)
		now = time.localtime()
		date = time.strftime('%a, %d %b %Y %H:%M:%S EST', now)
		date = str(date)
		f = open('measurements.txt', 'a')
		f.write(date + " " + data + "\n")
		f.close() # file is closed after each appended measurement to ensure it is saved
		print 'water logged'
	except:
		print('could not write to {0}').format(TEXTFILE)

while True:
	logMedian() # starts each set of measurements
	time.sleep(FREQUENCY_SECONDS) # time between each set of measurements



