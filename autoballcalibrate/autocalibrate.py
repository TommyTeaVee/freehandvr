from ast import literal_eval
from imutils.video import VideoStream
import cv2
import imutils
import numpy as np
import sys
import re
import time
## plan
## detect a ball first of all with opencv
## then sample a hue
## play around with values till good
## need to run this twice, one red and one blue
## usage: python autocalibrate.py color cameraNum (Ex. python autocalibrate.py red 0)
## add more color options
## specify red or blue

## when it detects 30 data points, jump out loop and start going on, average those values and continue

## TODO:
## 	CLEAN UP GUI
## SUPPRESS OUTPUT LATER ON UNLESS D IS SPECIFIED
## FIX COLOR OPTIONS
## OVERLAY TO ALERT USERS TO HOLD STILL
## add option after quitting to go to manual mode, will do later
## OUTLIER ISSUE
## OUTPUT IT TO FILE
## EXPAND HUE SAMPLING REGION
## PROPER EXITING
## TRY CATCH ALL PROBLEMS
## GET RID OF PRINT DEBUG
## BETTER CONVERSION SYSTEM

if len(sys.argv) != 3:
	print 'Wrong options'
	exit(1)

if "red" in sys.argv[1]:
	filename = 'red.txt'
else:
	filename = 'blue.txt'

number = int(re.search(r'\d+', sys.argv[2]).group())

data = []

while True:

	#read the image from the camera
	videoSrc = VideoStream(src=number).start()    
	
	#You will need this later
	frame = videoSrc.read()
	
	if frame is None:
		continue
	
	frame = imutils.resize(frame, width=600)
	
	gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
	## smooth and blur
	gray = cv2.GaussianBlur(gray,(5,5),0);
	gray = cv2.medianBlur(gray,7)
	
	# Adaptive Guassian Threshold is to detect sharp edges in the Image. For more information Google it.
	gray = cv2.adaptiveThreshold(gray,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,\
            cv2.THRESH_BINARY,11,3.5)
	## erode and dilate
	edit = cv2.erode(gray.copy(), None, iterations=5)
	edit = cv2.dilate(edit, None, iterations=5)
	## detect circles
	circles = cv2.HoughCircles(edit, cv2.HOUGH_GRADIENT, 1, 200, param1=30, param2=45, minRadius=0, maxRadius=200)
	if circles is not None:
		## convert the (x, y) coordinates and radius of the circles to integers
		circles = np.round(circles[0, :]).astype("int")
		## print 'YAYYYAYAYAYAY'
		for (x, y, r) in circles:
			# draw the circle in the output image, then draw a rectangle in the image
			# corresponding to the center of the circle
			cv2.circle(frame, (x, y), r, (0, 255, 0), 4)
			cv2.rectangle(frame, (x - 5, y - 5), (x + 5, y + 5), (0, 128, 255), -1)
			if x != 0 and y != 0:
				data.append((x,y,r))
	# Quit the program when Q is pressed
	cv2.imshow('Main Output', frame)
	cv2.imshow('Grayscale', gray)
	cv2.imshow('Calibrated Detection', edit)
	if len(data) >= 30:
		break
	if cv2.waitKey(1) & 0xFF == ord('q'):
		break
cv2.destroyAllWindows()
time.sleep(5)
if len(data) >= 30:
	avgX, avgY = 0, 0
	for i in range(len(data)):
		avgX += data[i][0]
		avgY += data[i][1]
	avgX = int(avgX / 30)
	avgY = int(avgY / 30)
	pixel = frame[avgX, avgY]
	blurred = cv2.GaussianBlur(frame, (11, 11), 0)
	hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)
	hsvPixel = hsv[avgX, avgY]
	lower = ((hsvPixel[0] - 10) if hsvPixel[0] >= 10 else 0, (hsvPixel[1] - 10) if hsvPixel[1] >= 10 else 0, (hsvPixel[2] - 40) if hsvPixel[2] >= 40 else 0)
	higher = (hsvPixel[0] + 10, hsvPixel[1] + 10, hsvPixel[2] + 40)
	#lower = (hsvPixel[0], hsvPixel[1], hsvPixel[2])
	lower = np.array(lower, np.uint8)
	higher = np.array(higher, np.uint8)
	## utilize the radius too
	print lower ## REMOVE LATER ON
	print higher
	while True:

		#read the image from the camera
		videoSrc = VideoStream(src=number).start()    

		#You will need this later
		frame = videoSrc.read()
		
		frame = imutils.resize(frame, width=600)
		blurred = cv2.GaussianBlur(frame, (11, 11), 0)
		hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)
		
		mask = cv2.inRange(hsv, lower, higher)
		mask = cv2.erode(mask, None, iterations=2)
		mask = cv2.dilate(mask, None, iterations=2)
		cv2.rectangle(hsv, (avgX - 5, avgY - 5), (avgX + 5, avgY + 5), (0, 128, 255), -1)
		cv2.imshow('Calibrated Detection', mask)
		cv2.imshow('Main Output', frame)
		cv2.imshow('HSV Output', hsv)
		if cv2.waitKey(1) & 0xFF == ord('q'):
			break
text_file = open(filename, "w")
text_file.close()
print 'values calibrated'
print pixel
print lower
print higher
for i in range(len(data)):
		print str(data[i][0]) + ", " + str(data[i][0])
cv2.destroyAllWindows()