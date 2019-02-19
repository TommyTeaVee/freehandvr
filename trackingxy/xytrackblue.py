from collections import deque
from ast import literal_eval
from imutils.video import VideoStream
from threading import Thread
import numpy as np
import cv2
import imutils
import time
import socket
import sys
import getopt

## sending all 2d coordinates, Unity dealing with averages
data = deque([])
IP = '127.0.0.1'

def socketSend(UDP_PORT):
	sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	while True:
		try:
			temp = data.popleft()
			sock.sendto((temp).encode(), (IP, UDP_PORT))
		except Exception as e:
			continue

if __name__ == '__main__':
	camera, port = None, None
	debug = 0
	blueLower = None
	try:
		opts, args = getopt.getopt(sys.argv[1:], 'c:p:db:', ['camera=', 'port=', 'debug', 'blue='])
	except getopt.GetoptError:
		print 'Wrong options'
		exit(1)
	for opt, arg in opts:
		if opt in ('-c', '--camera'):
			camera = arg
		if opt in ('-p', '--port'):
			port = int(arg)
		if opt in ('-d', '--debug'):
			debug = 1
		if opt in ('-b', '--blue'):
			blueLower = literal_eval(arg)
	## optimized HSV values for red and blue
	
	if blueLower is None:
		blueLower = (90, 170, 60)
	
	upper = (255, 255, 255)
	videoSrc = VideoStream(src=int(camera)).start()
	## camera warm up for 2 seconds
	time.sleep(2.0)
	## start thread to send UDP data
	dataSender = Thread(target=socketSend, args=(port,))
	dataSender.start()
	## constant looping, no exit allowed, must be terminated by unity
	while True:
		# grab the current frame
		frame = videoSrc.read()
 
		# resize the frame, blur it, and convert it to the HSV color space
		frame = imutils.resize(frame, width=600)
		blurred = cv2.GaussianBlur(frame, (11, 11), 0)
		hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)
 
		## now for blue
		# construct a mask for the color "blue", then perform and then erode and dilate to make smoother
		mask = cv2.inRange(hsv, blueLower, upper)
		mask = cv2.erode(mask, None, iterations=2)
		mask = cv2.dilate(mask, None, iterations=2)
		# find contours in the mask and initialize the current and initialize (x, y) center of the ball
		cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,
			cv2.CHAIN_APPROX_SIMPLE)
		cnts = imutils.grab_contours(cnts)
		center = None
 
		# only proceed if at least one contour was found
		if len(cnts) > 0:
			# find the largest contour in the mask, then use
			# it to compute the minimum enclosing circle and
			# centroid
			c = max(cnts, key=cv2.contourArea)
			((blueX, blueY), radius) = cv2.minEnclosingCircle(c)
			M = cv2.moments(c)
			center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
 
		# only proceed if the radius meets a minimum size
			if radius > 12:
				# draw the circle and centroid on the frame,
				# then update the list of tracked points
				cv2.circle(frame, (int(blueX), int(blueY)), int(radius),
					(255, 0, 0), 2)
				cv2.circle(frame, center, 5, (255, 255, 255), -1)
				strBlue = 'Blue (x, y): ' + str(int(blueX)) + ', ' + str(int(blueY))
				data.append(strBlue)
				if debug is 1:
					print strBlue
		# show the frame to our screen
		if debug is 1:
			cv2.imshow("Frame", frame)
			key = cv2.waitKey(1) & 0xFF