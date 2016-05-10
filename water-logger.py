import RPi.GPIO as GPIO
import json
import sys
import time
from time import localtime
from time import sleep
import datetime
import csv
import os
import sys
import picam


# wait for time to be set to realtime
sleep(5) 

# period in between measurments
FREQUENCY_SECONDS = 60 * 5

# set pinmode
GPIO.setmode(GPIO.BCM)

# distance sensor pins
TRIG = 23
ECHO = 24
DELAY = 60*10

# shutdown button
GPIO.setup(18,GPIO.IN)

print 'Press Ctrl-C to quit.'

# a detailed description of how this function works is available in the modmypi tutorial
def distance(): 
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
	# set the current directory for the data to todays date
	day = str(time.strftime("%m-%d-%Y"))
	directory = '/media/pi/SANDISK/' + day
	photodir = directory + "/photos"
	filename = str(directory + "/" + day +'.csv')
	print directory
	
	# check if directories exist
	# create them if they do not
	if os.path.exists(directory) == False:
	    os.makedirs(directory)
	    print "created directory"
	if os.path.exists(photodir) == False:
	    os.makedirs(photodir)
	    print "created directory"

	# create an empty array to store the measurements
	data = []
	loop = 0
	print 'beginning measurements'

	# measure water level X amount of times 
	while loop <= 8 :
		m = distance()
		data.append(m)
		print "measured {0} times".format(loop)
		loop = loop + 1

	# sort the data by distance and grab the media value to help ensure accuracy
	print data
	data.sort()
	median = str(data[4])

	# log the current time and measurment to a spreadsheet
	with open(filename, 'a') as fp:
	    writer = csv.writer(fp, dialect='excel', delimiter=',')
	    timestamp = str(time.strftime("%m/%d, %H:%M"))
	    writer.writerow([timestamp, median])
	    print 'water logged'

	# take a photo of the drain. Label it the row number of the corresponding measurement
	row_count = 0
	with open(filename, 'r') as f:
		reader = csv.DictReader(f)
		for row in reader:
			row_count += 1
		row_count = str(row_count)
		photo = picam.takePhotoWithDetails(640,480, 85)
		photo.save(photodir+"/"+row_count+".jpg")
	

# neverending loop	
while True:
	# check if the shutdown switch is on
	button_current = GPIO.input(18)
	if (button_current):
		# shutdown the pi if it is
		print "shutting down now"
		os.system("sudo shutdown -h now")
		sleep(1)

	# call the function to log data
	logMedian()
	sleep(FREQUENCY_SECONDS)
