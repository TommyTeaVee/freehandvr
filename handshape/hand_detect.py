import cv2
import numpy as np
import copy
import math

# Environment:
# OS    : Windows 10
# python: 2.7
# opencv: 3.4.0
# Lukas 2/16/19

lowB = 255;
lowG = 255;
lowR = 255;

highB = 0;
highG = 0;
highR = 0;

stepNum = 0;

while stepNum == 0:

    # Open Camera
    camera = cv2.VideoCapture(0)
    camera.set(10, 200) 

    while camera.isOpened():

        #Main Camera
        ret, frame = camera.read()
        frame = cv2.bilateralFilter(frame, 5, 50, 100)  # Smoothing
        frame = cv2.flip(frame, 1)  #Horizontal Flip

        k = cv2.waitKey(10)
        if k == 27:  # press ESC to exit
            break

        cv2.putText(frame, 'O', (300, 110), cv2.FONT_ITALIC, 0.3, 255)
        cv2.putText(frame, 'O', (225, 135), cv2.FONT_ITALIC, 0.3, 255)
        cv2.putText(frame, 'O', (385, 140), cv2.FONT_ITALIC, 0.3, 255)
        cv2.putText(frame, 'O', (460, 215), cv2.FONT_ITALIC, 0.3, 255)
        cv2.putText(frame, 'O', (100, 285), cv2.FONT_ITALIC, 0.3, 255)
        cv2.putText(frame, 'O', (310, 350), cv2.FONT_ITALIC, 0.3, 255)
        cv2.imshow('Video', frame)

        color = frame[300, 110]
        rVal = color[0].asType(numpy.int)
        gVal = color[1]
        bVal = color[2]

        ret, frame2 = camera.read()
        frame2 = cv2.bilateralFilter(frame2, 5, 50, 100)  # Smoothing
        frame2 = cv2.flip(frame2, 1)

        font = cv2.FONT_HERSHEY_SIMPLEX

        print "" + rVal

        cv2.putText(frame2,'OpenCV Tuts!',(300,110), font, 1, (rVal,gVal,bVal), 2, cv2.LINE_AA)

        cv2.imshow('Color', frame2)

        '''
        color = frame[300, 110]
        
        if color[0] < lowB :
            lowB = color[0]

        if color[1] < lowG :
            lowG = color[1]

        if color[2] < lowR :
            lowR = color[2]

        if color[0] > highB :
            highB = color[0]

        if color[1] > highG :
            highG = color[1]

        if color[2] > highR :
            highR = color[2]

        color = frame[225, 135]
        
        if color[0] < lowB :
            lowB = color[0]

        if color[1] < lowG :
            lowG = color[1]

        if color[2] < lowR :
            lowR = color[2]

        if color[0] > highB :
            highB = color[0]

        if color[1] > highG :
            highG = color[1]

        if color[2] > highR :
            highR = color[2]

        color = frame[385, 140]
        
        if color[0] < lowB :
            lowB = color[0]

        if color[1] < lowG :
            lowG = color[1]

        if color[2] < lowR :
            lowR = color[2]

        if color[0] > highB :
            highB = color[0]

        if color[1] > highG :
            highG = color[1]

        if color[2] > highR :
            highR = color[2]

        color = frame[460, 215]
        
        if color[0] < lowB :
            lowB = color[0]

        if color[1] < lowG :
            lowG = color[1]

        if color[2] < lowR :
            lowR = color[2]

        if color[0] > highB :
            highB = color[0]

        if color[1] > highG :
            highG = color[1]

        if color[2] > highR :
            highR = color[2]

        color = frame[100, 285]
        
        if color[0] < lowB :
            lowB = color[0]

        if color[1] < lowG :
            lowG = color[1]

        if color[2] < lowR :
            lowR = color[2]

        if color[0] > highB :
            highB = color[0]

        if color[1] > highG :
            highG = color[1]

        if color[2] > highR :
            highR = color[2]

        color = frame[310, 350]
        
        if color[0] < lowB :
            lowB = color[0]

        if color[1] < lowG :
            lowG = color[1]

        if color[2] < lowR :
            lowR = color[2]

        if color[0] > highB :
            highB = color[0]

        if color[1] > highG :
            highG = color[1]

        if color[2] > highR :
            highR = color[2]

        print "LOW: "
        print lowR
        print lowG
        print lowB

        print "HIGH: "
        print highR
        print highG
        print highB
    '''
while stepNum == 1:

    # Open Camera
    camera = cv2.VideoCapture(0)
    camera.set(10, 200) 

    def calculateFingers(res, drawing):
        # convexity defect
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
                        if cnt < 4:
                            cnt += 1
                            cv2.circle(drawing, far, 8, [211, 84, 0], -1)
                if cnt > 0:
                    if cnt < 6:
                        return True, cnt+1
                else:
                    return True, 0
        return False, 0

    while camera.isOpened():

        #Main Camera
        ret, frame = camera.read()
        frame = cv2.bilateralFilter(frame, 5, 50, 100)  # Smoothing
        frame = cv2.flip(frame, 1)  #Horizontal Flip
        #cv2.imshow('original', frame)

        #Background Removal
        bgModel = cv2.createBackgroundSubtractorMOG2(0, 50)
        fgmask = bgModel.apply(frame)

        kernel = np.ones((3, 3), np.uint8)
        fgmask = cv2.erode(fgmask, kernel, iterations=1)
        img = cv2.bitwise_and(frame, frame, mask=fgmask)

        # Skin detect and thresholding
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        lower = np.array([100, 100, 100], dtype="uint8")
        upper = np.array([255, 255, 255], dtype="uint8")
        skinMask = cv2.inRange(hsv, lower, upper)
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
            print "Fingers", cnt
            cv2.imshow('output', drawing)

        k = cv2.waitKey(10)
        if k == 27:  # press ESC to exit
            break

        cv2.putText(frame, 'O', (300, 110), cv2.FONT_ITALIC, 0.3, 255)
        cv2.putText(frame, 'O', (225, 135), cv2.FONT_ITALIC, 0.3, 255)
        cv2.putText(frame, 'O', (385, 140), cv2.FONT_ITALIC, 0.3, 255)
        cv2.putText(frame, 'O', (460, 215), cv2.FONT_ITALIC, 0.3, 255)
        cv2.putText(frame, 'O', (100, 285), cv2.FONT_ITALIC, 0.3, 255)
        cv2.putText(frame, 'O', (310, 350), cv2.FONT_ITALIC, 0.3, 255)
        cv2.imshow('Video', frame);

