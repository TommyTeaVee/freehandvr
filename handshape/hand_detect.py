from collections import deque
from threading import Thread
from ast import literal_eval
import cv2
import numpy as np
import copy
import math
import time
import socket
import sys
import getopt

# Environment:
# OS    : Windows 10
# python: 2.7
# opencv: 3.4.0
# Lukas 2/16/19

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

def calculateFingers(res, drawing):
    #  convexity defect
    hull = cv2.convexHull(res, returnPoints=False)
    if len(hull) > 3:
        defects = cv2.convexityDefects(res, hull)
        if defects is not None:
            cnt = 0
            for i in range(defects.shape[0]):  # calculate the angle
                s, e, f, d = defects[i][0]
                start = tuple(res[s][0])
                end = tuple(res[e][0])
                far = tuple(res[f][0])
                a = math.sqrt((end[0] - start[0]) ** 2 + (end[1] - start[1]) ** 2)
                b = math.sqrt((far[0] - start[0]) ** 2 + (far[1] - start[1]) ** 2)
                c = math.sqrt((end[0] - far[0]) ** 2 + (end[1] - far[1]) ** 2)
                angle = math.acos((b ** 2 + c ** 2 - a ** 2) / (2 * b * c))  # cosine theorem
                if angle <= math.pi / 2:  # angle less than 90 degree, treat as fingers
                    cnt += 1
                    cv2.circle(drawing, far, 8, [211, 84, 0], -1)
            if cnt > 0:
                return True, cnt+1
            else:
                return True, 0
    return False, 0

if __name__ == '__main__':
	cam, port = None, None
	debug = 0
	low, high = None, None
	try:
		opts, args = getopt.getopt(sys.argv[1:], 'c:p:dl:h:', ['camera=', 'port=', 'debug', 'low=', 'high='])
	except getopt.GetoptError:
		print 'Wrong options'
		exit(1)
	for opt, arg in opts:
		if opt in ('-c', '--camera'):
			cam = arg
		if opt in ('-p', '--port'):
			port = int(arg)
		if opt in ('-d', '--debug'):
			debug = 1
		if opt in ('-l', '--low'):
			low = literal_eval(arg)
		if opt in ('-h', '--high'):
			high = literal_eval(arg)
	camera = cv2.VideoCapture(int(cam))
	camera.set(10, 200)
	dataSender = Thread(target=socketSend, args=(port,))
	dataSender.start()
	if low is None:
		low = (30, 30, 80)
	if high is None:
		high = (180, 180, 255)
	while camera.isOpened():
		#Main Camera
		ret, frame = camera.read()
		frame = cv2.bilateralFilter(frame, 5, 50, 100)  # Smoothing
		frame = cv2.flip(frame, 1)  #Horizontal Flip
		if debug is 1:
			cv2.imshow('original', frame)
	
	
		#Background Removal
		bgModel = cv2.createBackgroundSubtractorMOG2(0, 50)
		fgmask = bgModel.apply(frame)
	
		kernel = np.ones((3, 3), np.uint8)
		fgmask = cv2.erode(fgmask, kernel, iterations=1)
		img = cv2.bitwise_and(frame, frame, mask=fgmask)
	
		# Skin detect and thresholding
		hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
		lower = np.array([low[0], low[1], low[2]], dtype="uint8")
		upper = np.array([high[0], high[1], high[2]], dtype="uint8")
		skinMask = cv2.inRange(hsv, lower, upper)
		if debug is 1:
			cv2.imshow('Threshold Hands', skinMask)
	
		# Getting the contours and convex hull
		skinMask1 = copy.deepcopy(skinMask)
		_,contours, hierarchy = cv2.findContours(skinMask1, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
		length = len(contours)
		maxArea = -1
		if length > 0:
			for i in xrange(length):
				temp = contours[i]
				area = cv2.contourArea(temp)
				if area > maxArea:
					maxArea = area
					ci = i

			res = contours[ci]
			hull = cv2.convexHull(res)
			drawing = np.zeros(img.shape, np.uint8)
			cv2.drawContours(drawing, [res], 0, (0, 255, 0), 2)
			cv2.drawContours(drawing, [hull], 0, (0, 0, 255), 3)

			isFinishCal, cnt = calculateFingers(res, drawing)
			if cnt <= 5:
				data.append(str(cnt))
			if debug is 1:
				if cnt <= 5:
					print "Fingers", cnt
				cv2.imshow('output', drawing)

		k = cv2.waitKey(10)

