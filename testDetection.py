# import the necessary packages
import numpy as np
import time
import cv2
import os
import imutils

myFPS = 0
myFrame = 0

myConfidence = 0.76
myThreshold = 0.4

limitCPUtemp = True
cpuTempLimit = 54
limitToVideoFPS = False

# createOutput = True
createOutput = False

# Limit CPU usage by sleeping for 1 second after every loop
# device = "pi"
device = "pc"

# Zeige Kamerabild, kein DNN Durchlauf
# testCameraWithoutDNN = True
testCameraWithoutDNN = False

if(device is "pi"):
	from gpiozero import CPUTemperature
	# limitToVideoFPS = True
	myWidth = 500
	myHeight = 350

if(device is "pc"):
	limitToVideoFPS = True
	myWidth = 1280
	myHeight = 720
	# myWidth = 720
	# myHeight = 1280
	

# Networks
networks = {}
networks["64_v6"] = {"folder": "64_v6", "resolution": 64, "weights": "team5_62100.weights"}
networks["64_v5"] = {"folder": "64_v5", "resolution": 64, "weights": "team5_14000.weights"}
networks["64_v4"] = {"folder": "64_v4", "resolution": 64, "weights": "yolov3-tiny_last.weights"}
networks["64_v3"] = {"folder": "64_v3", "resolution": 64, "weights": "yolov3-tiny_last.weights"}
networks["64_v2"] = {"folder": "64_v2", "resolution": 64, "weights": "yolov3-tiny_last.weights"}
networks["64"] = {"folder": "64", "resolution": 64, "weights": "yolov3-tiny_16500.weights"}
networks["128"] = {"folder": "128", "resolution": 128, "weights": "yolov3-tiny_2000.weights"}
networks["256_1st"] = {"folder": "256_1st", "resolution": 256, "weights": "yolov3-tiny_last.weights"}
networks["256_2nd"] = {"folder": "256_2nd", "resolution": 256, "weights": "yolov3-tiny_last.weights"}
networks["416"] = {"folder": "416", "resolution": 416, "weights": "yolov3-tiny_last.weights"}

selectedNetwork = networks["64_v6"]
# selectedNetwork = networks["64_v5"]
# selectedNetwork = networks["64_v4"]

# Video Inputs

# Raspi hell
# myInput = "../videos/original/2019-07-07_21_20_37_1080p30.mp4"
# myInput = "../videos/cut_1.mkv"
# myInput = "../videos/cut_2.mkv"
# myInput = "../videos/cut_3.mkv"
# myInput = "../videos/cut_2019-01-24_00_34_57_720p60.mkv"
myInput = "../videos/cut_2019-01-24_00_06_01_720p10.mkv"
# myInput = "../videos/cut_2019-01-20_20_10_45_720p60.mkv"

# Raspi dunkel
# myInput = "../videos/cut_2019-01-20_20_02_47_720p60.mkv"

# Smartphone
# myInput = "../videos/cut_20190121_093412.mkv"
# myInput = "../videos/cut_20190121_094127.mkv"
# myInput = "../videos/cut_20190124_115512.mkv"
# myInput = "../videos/original/Flo/IMG_1157.MOV"
# myInput = "../videos/original/flo/IMG_1158.MOV"
# myInput = "../videos/cut_steffen.mkv"
# myInput = "../videos/nadine_1.mp4"

# myInput = "../videos/test-video1.mp4"
# myInput = "../videos/test-video2.mp4"
# 0 und 1 sind die Webcams
# myInput = 0
# myInput = 1
myOutput = "output.mp4"

myDNNsize = selectedNetwork["resolution"]

winname = selectedNetwork["folder"]
cv2.namedWindow(winname)
cv2.moveWindow(winname, 10, 10)

# load the COCO class labels our YOLO model was trained on
labelsPath = os.path.sep.join(["classes\yolov3", selectedNetwork["folder"], "team5.names"])
LABELS = open(labelsPath).read().strip().split("\n")

# initialize a list of colors to represent each possible class label
np.random.seed(42)
COLORS = np.random.randint(0, 255, size=(len(LABELS), 3), dtype="uint8")

# derive the paths to the YOLO weights and model configuration
weightsPath = os.path.sep.join(["classes\yolov3", selectedNetwork["folder"], selectedNetwork["weights"] ])
configPath = os.path.sep.join(["classes\yolov3", selectedNetwork["folder"], "team5.cfg"])

# load our YOLO object detector trained on COCO dataset (80 classes)
# and determine only the *output* layer names that we need from YOLO
print("[INFO] loading YOLO from disk...")
print(configPath, weightsPath)
net = cv2.dnn.readNetFromDarknet(configPath, weightsPath)
ln = net.getLayerNames()
ln = [ln[i[0] - 1] for i in net.getUnconnectedOutLayers()]

writer = None
(W, H) = (None, None)

# initialize the video stream, pointer to output video file, and
# frame dimensions
vs = cv2.VideoCapture(myInput)
fps = vs.get(cv2.CAP_PROP_FPS)

if(myInput is 0 or myInput is 1):
	# vs.set(cv2.CV_CAP_PROP_BUFFERSIZE, 1)
	vs.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
	vs.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
	vs.set(cv2.CAP_PROP_FPS, 30)
	# vs.open(0)

# Camera test
if testCameraWithoutDNN is True:
	while True:
		(grabbed, frame) = vs.read()

		if not grabbed:
			break
		
		frame = imutils.resize(frame, height=myHeight, width=myWidth)
		cv2.imshow(selectedNetwork["folder"],frame)

		if cv2.waitKey(1) & 0xFF == ord('q'):
			break
	exit()

# loop over frames from the video file stream
while True:
	if limitCPUtemp is True and device is "pi":
		# CPU temp
		cpu = CPUTemperature()
		cpuTemp = cpu.temperature
		print(cpuTemp)
		while cpuTemp > cpuTempLimit:
			time.sleep(0.1)
			cpuTemp = cpu.temperature
			print("cooling down...")
			print(cpuTemp)

	# um ein möglichst aktuelles Camera-Bild zu analysieren/anzeigen werden mehrere Frames übersprungen
	# CameraFPS/5 = Anzahl geskippter Frames; bei 30FPS werden also 6 Frames pro Schleifendurchlauf verarbeitet wovon die ersten 5 verworfen werden
	if(device is "pi" and (myInput is 0 or myInput is 1) ):
		numberOfFramesToSkip = 1
		if fps > 0:
			numberOfFramesToSkip = (int)(fps/5)
		for x in range(numberOfFramesToSkip):
			(grabbed, frame) = vs.read()
	else:
		# read the next frame from the file
		(grabbed, frame) = vs.read()

	# (grabbed, frame) = vs.read()

	# if the frame was not grabbed, then we have reached the end
	# of the stream
	if not grabbed:
		break
	
	# frame = frame[my_y:my_y+my_h, my_x:my_x+my_w]

	# if the frame dimensions are empty, grab them
	if W is None or H is None:
		(H, W) = frame.shape[:2]

	start = time.time()

	# construct a blob from the input frame and then perform a forward
	# pass of the YOLO object detector, giving us our bounding boxes
	# and associated probabilities
	blob = cv2.dnn.blobFromImage(frame, 1 / 255.0, (myDNNsize, myDNNsize),
		swapRB=True, crop=False)
	net.setInput(blob)
	
	# most CPU intensive part!
	layerOutputs = net.forward(ln)
	
	# initialize our lists of detected bounding boxes, confidences,
	# and class IDs, respectively
	boxes = []
	confidences = []
	classIDs = []

	# loop over each of the layer outputs
	for output in layerOutputs:
		# loop over each of the detections
		for detection in output:
			# extract the class ID and confidence (i.e., probability)
			# of the current object detection
			scores = detection[5:]
			classID = np.argmax(scores)
			confidence = scores[classID]

			# filter out weak predictions by ensuring the detected
			# probability is greater than the minimum probability
			if confidence > myConfidence:
				# scale the bounding box coordinates back relative to
				# the size of the image, keeping in mind that YOLO
				# actually returns the center (x, y)-coordinates of
				# the bounding box followed by the boxes' width and
				# height
				box = detection[0:4] * np.array([W, H, W, H])
				(centerX, centerY, width, height) = box.astype("int")

				# use the center (x, y)-coordinates to derive the top
				# and and left corner of the bounding box
				x = int(centerX - (width / 2))
				y = int(centerY - (height / 2))

				# update our list of bounding box coordinates,
				# confidences, and class IDs
				boxes.append([x, y, int(width), int(height)])
				confidences.append(float(confidence))
				classIDs.append(classID)
				

	# apply non-maxima suppression to suppress weak, overlapping
	# bounding boxes
	idxs = cv2.dnn.NMSBoxes(boxes, confidences, myConfidence, myThreshold)
	
	# ensure at least one detection exists
	if len(idxs) > 0:
		# loop over the indexes we are keeping
		for i in idxs.flatten():
			# extract the bounding box coordinates
			(x, y) = (boxes[i][0], boxes[i][1])
			(w, h) = (boxes[i][2], boxes[i][3])

			# draw a bounding box rectangle and label on the frame
			color = [int(c) for c in COLORS[classIDs[i]]]
			cv2.rectangle(frame, (x, y), (x + w, y + h), color, 8)
			text = "{}: {:.4f}".format(LABELS[classIDs[i]],
				confidences[i])
			cv2.putText(frame, text, (x, y - 5),
				cv2.FONT_HERSHEY_SIMPLEX, 1.3, color, 4)
	
	# check if the video writer is None
	if createOutput is True:
		if writer is None:
			# initialize our video writer
			fourcc = cv2.VideoWriter_fourcc(*"X264")
			writer = cv2.VideoWriter(myOutput, fourcc, 30,
				(frame.shape[1], frame.shape[0]), True)
		# write the output frame to disk
		writer.write(frame)

	# 	# some information on processing single frame
	
	myFrame += 1
	end = time.time()
	elap = (end - start)
	myFPS = "{:.2f}".format(1/elap)

	if(limitToVideoFPS == True):
		# print("Sleep um die CPU Temperatur in den Griff zu bekommen")
		# time.sleep(0.01)

		# Limitierung auf Video FPS
		timeToSleepForFPS = (1 / fps)
		if( timeToSleepForFPS>elap ):
			timeToSleepForFPS -= elap
		time.sleep(timeToSleepForFPS)

	# if(device == "pi" and limitToVideoFPS == True):
	# 	time.sleep(0.1)

	# print("[INFO] single frame took {:.4f} seconds".format(elap))
	# print("FPS without limit: "+myFPS)
	cv2.putText(frame, "DNN FPS: "+myFPS, (5, 50), cv2.FONT_HERSHEY_SIMPLEX, 1.4, (0,255,0), 4)
	cv2.putText(frame, "input FPS: {:.2f}".format(fps), (5, 100), cv2.FONT_HERSHEY_SIMPLEX, 1.4, (0,255,0), 4)

	frame = imutils.resize(frame, height=myHeight, width=myWidth)
	cv2.imshow(selectedNetwork["folder"],frame)

	if cv2.waitKey(1) & 0xFF == ord('q'):
		break

vs.release()
cv2.destroyAllWindows()