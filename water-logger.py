import RPi.GPIO as GPIO
import json
import sys
import time
from time import localtime
import datetime
import csv
import os
import sys
import picam

FREQUENCY_SECONDS      = 5

GPIO.setmode(GPIO.BCM)

# pins thge pi uses to communicate with the distance sensor
TRIG = 23
ECHO = 24

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
	day = str(time.strftime("%d-%m-%Y"))
	directory = '/media/pi/SANDISK/' + day
	photodir = directory + "/photos"
	filename = str(directory + "/" + day +'.csv')
	print directory
	
	if os.path.exists(directory) == False:
	    os.makedirs(directory)
	    print "created directory"
	if os.path.exists(photodir) == False:
	    os.makedirs(photodir)
	    print "created directory"

	data = []
	loop = 0
	print 'beginning measurements'
	while loop < 3:
		m = distance()
		data.append(m)
		print "measured {0} times".format(loop)
		loop = loop + 1
	print data
	data.sort()
	median = str(data[1])

	with open(filename, 'a') as fp:
	    writer = csv.writer(fp, dialect='excel', delimiter=',')
	    timestamp = str(time.strftime("%m/%d, %H:%M"))
	    writer.writerow([timestamp, median])
	    print 'water logged'

	row_count = 0
	with open(filename, 'r') as f:
		reader = csv.DictReader(f)
		for row in reader:
			row_count += 1
		row_count = str(row_count)
		photo = picam.takePhotoWithDetails(640,480, 85)
		photo.save(photodir+"/"+row_count+".jpg")
	
	

logMedian()
