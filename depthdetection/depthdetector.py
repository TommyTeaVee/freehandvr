from ast import literal_eval
from collections import deque
from imutils.video import VideoStream
from threading import Thread
import numpy as np
import cv2
import imutils
import time
import socket
import sys
import getopt

## blue ball must depth perception

## sending scaled depth
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
	camera, port, blueLower = None, None, None
	debug = 0
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
	## optimized HSV values for blue
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
 
		# construct a mask for the color "red", then perform and then erode and dilate to make smoother
		mask = cv2.inRange(hsv, blueLower, upper)
		mask = cv2.erode(mask, None, iterations=2)
		mask = cv2.dilate(mask, None, iterations=2)
		# find contours in the mask and initialize the current and initialize (x, y) center of the ball
		pixelCount = cv2.countNonZero(mask)
		# using inverse of formula detected via data collections
		try:
			distance = 209.482/(pow(pixelCount, 0.3362474781439139))
			data.append(distance)
		except Exception as e:
			distance = 'Unavailable'
		# show the rame to our screen
		if debug is 1:
			cv2.imshow("Frame", frame)
			key = cv2.waitKey(1) & 0xFF
			cv2.imshow("Threshold", mask)
			print distance