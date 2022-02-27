import cvzone
from cvzone.HandTrackingModule import HandDetector
import cv2
import pyaudio
import audioop

p = pyaudio.PyAudio()

CHUNK = 1024 * 2
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100

cap = cv2.VideoCapture(0) 

det = HandDetector(detectionCon=0.75)


# stream object to get data from microphone
stream = p.open(
	format=FORMAT,
	channels=CHANNELS,
	rate=RATE,
	input=True,
	output=True,
	frames_per_buffer=CHUNK
)

canvas = cv2.imread("transparent.png")


isOn = 0

color = [[0,255,255],[255,0,0]]

while True:
	global count
	count = 0
	try:
		success, img = cap.read()
		h, w, layers = img.shape
		resized_w = w * 1.2
		resized_h = h * 1.2
		img = cv2.resize(img, (int(resized_w), int(resized_h)))
		canvas = cv2.resize(canvas, (img.shape[1], img.shape[0]))
		img = cv2.flip(img, 1)
		hands = det.findHands(img, draw=False)
		img = cv2.addWeighted(canvas, 1, img, 0.9, 5)
		if len(hands) >= 1:
			if (det.fingersUp(hands[0]) == [0, 1, 0, 0, 0]):
				print("draw")
				lmList = hands[0]["lmList"]
				x, y = lmList[8][:2]
				print(lmList[8][:2])
				cv2.circle(canvas,(int(x), int(y)), 10, color[isOn], cv2.FILLED)
				print(det.fingersUp(hands[0]))
			if (det.fingersUp(hands[0]) == [0, 1, 1, 1, 0]):
				canvas = cv2.imread("transparent.png")

		cv2.imshow("Img", img)
		cv2.waitKey(1)

		data = stream.read(CHUNK)
		rms = audioop.rms(data, 2)
		if ((rms>7000) and (rms<8000)):
			if (isOn == 0): 
				isOn = 1
			elif (isOn == 1):
				isOn = 0
			print(isOn)
	except KeyboardInterrupt:
		print("okay done")