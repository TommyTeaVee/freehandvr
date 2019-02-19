## detect and display an image from all cameras

from imutils.video import VideoStream
import cv2
import imutils

index = 0
arr = []
while True:
    cap = cv2.VideoCapture(index)
    if not cap.read()[0]:
        break
    else:
        arr.append(index)
    cap.release()
    index += 1

videoSrc = []

for j in range(len(arr)):
		videoSrc.append(VideoStream(src=int(arr[j])).start())
name = []
for j in range(len(arr)):
	name.append("Camera " + str(arr[j]))
frame = [None] * len(arr)
while True:
	for j in range(len(arr)):
		frame[j] = videoSrc[j].read()
		frame[j] = imutils.resize(frame[j], width=600)
	for j in range(len(arr)):
		cv2.imshow(name[j], frame[j])
	if cv2.waitKey(1) & 0xFF == ord('q'):
		break
cv2.destroyAllWindows()