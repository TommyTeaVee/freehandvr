from collections import deque

from imutils.video import VideoStream

import numpy as np

import cv2

import imutils

import time

import socket

import sys

import getopt



## sending all 2d coordinates, Unity dealing with averages



IP = '127.0.0.1'



def socketSend(UDP_PORT):

	sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

	sock.sendto(("JUMP!").encode(), (IP, UDP_PORT))



if __name__ == '__main__':
	camera, port = None, None

	debug = 0

	try:

		opts, args = getopt.getopt(sys.argv[1:], 'c:p:d', ['camera=', 'port=', 'debug'])

	except getopt.GetoptError:

		exit(1)

	for opt, arg in opts:

		if opt in ('-c', '--camera'):

			camera = arg

		if opt in ('-p', '--port'):

			port = arg

		if opt in ('-d', '--debug'):

			debug = 1

	## optimized HSV values for red and blue

	redLower = (170, 150, 60)

	blueLower = (90, 170, 60)

	upper = (255, 255, 255)

	videoSrc = VideoStream(src=int(camera)).start()

	## camera warm up for 2 seconds

	time.sleep(2.0)

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

		
		# cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
		
		print cv2.countNonZero(mask)
		
		#if cnts is not None:
		#	for hold, arg in cnts:
		#		print cv2.contourArea(cv2.moments(hold))
			
		#print cv2.contourArea(cnts)
		# show the frame to our screen

		if debug is 1:

			cv2.imshow("Frame", frame)
			cv2.imshow("Threshold", mask)

			key = cv2.waitKey(1) & 0xFF