from ast import literal_eval
from imutils.video import VideoStream
import cv2
import imutils
import numpy as np
import sys
import re
## plan
## detect a ball first of all with opencv
## then sample a hue
## play around with values till good
## need to run this twice, one red and one blue
## SUPPRESS OUTPUT LATER ON UNLESS D IS SPECIFIED
## usage: python autocalibrate.py color cameraNum (Ex. python autocalibrate.py red 0)
## add more color options
## specify red or blue

## when it detects 50 data points, jump out loop and start going on, average those values and continue

if len(sys.argv) != 3:
	print 'Wrong options'
	exit(1)

if "red" in sys.argv[1]:
	filename = 'red.txt'
else:
	filename = 'blue.txt'

number = int(re.search(r'\d+', sys.argv[2]).group())

while True:

	#read the image from the camera
	videoSrc = VideoStream(src=number).start()    
	
	#You will need this later
	frame = videoSrc.read()
		
	frame = imutils.resize(frame, width=600)
	
	gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
	## smooth and blur
	gray = cv2.GaussianBlur(gray,(5,5),0);
	gray = cv2.medianBlur(gray,5)
	
	# Adaptive Guassian Threshold is to detect sharp edges in the Image. For more information Google it.
	gray = cv2.adaptiveThreshold(gray,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,\
            cv2.THRESH_BINARY,11,3.5)
	## erode and dilate
	gray = cv2.erode(gray, None, iterations=5)
	gray = cv2.dilate(gray, None, iterations=5)
	## detect circles
	circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, 1, 200, param1=30, param2=45, minRadius=0, maxRadius=200)
	if circles is not None:
		## convert the (x, y) coordinates and radius of the circles to integers
		circles = np.round(circles[0, :]).astype("int")
		## print 'YAYYYAYAYAYAY'
		for (x, y, r) in circles:
			# draw the circle in the output image, then draw a rectangle in the image
			# corresponding to the center of the circle
			cv2.circle(frame, (x, y), r, (0, 255, 0), 4)
			cv2.rectangle(frame, (x - 5, y - 5), (x + 5, y + 5), (0, 128, 255), -1)
	# Quit the program when Q is pressed
	cv2.imshow('Main Output', frame)
	cv2.imshow('Calibrated Detection', gray)
	if cv2.waitKey(1) & 0xFF == ord('q'):
		break

text_file = open(filename, "w")

## add option after quitting to go to manual mode, will do later