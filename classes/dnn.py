import numpy as np
import time, os
import cv2, imutils
import config as cfg

class Dnn:
    def __init__(self, liveview):
        self.liveview = liveview
        print("DNN started.")
        
    def processImageWithDNN(self, frame):
        myFPS = 0
        myFrame = 0

        myConfidence = 0.51
        myThreshold = 0.4

        networks = cfg.networks
        selectedNetwork = cfg.selectedNetwork

        # Input
        myInput = frame

        # YoloV3 network configurations
        myDNNsize = selectedNetwork["resolution"]
        myYolo = "classes/yolov3/"+selectedNetwork["folder"]+"/"
        labelsPath = os.path.sep.join([myYolo, "team5.names"])
        LABELS = open(labelsPath).read().strip().split("\n")

        # initialize a list of colors to represent each possible class label
        np.random.seed(42)
        COLORS = np.random.randint(0, 255, size=(len(LABELS), 3), dtype="uint8")

        # derive the paths to the YOLO weights and model configuration
        weightsPath = os.path.sep.join([myYolo, selectedNetwork["weights"]])
        configPath = os.path.sep.join([myYolo, "team5.cfg"])

        # read DNN weights
        net = cv2.dnn.readNetFromDarknet(configPath, weightsPath)
        ln = net.getLayerNames()
        ln = [ln[i[0] - 1] for i in net.getUnconnectedOutLayers()]

        (W, H) = (None, None)
        
        if W is None or H is None:
            (H, W) = frame.shape[:2]

        start = time.time()

        # construct a blob from the input frame and then perform a forward
        # pass of the YOLO object detector, giving us our bounding boxes
        # and associated probabilities
        blob = cv2.dnn.blobFromImage(frame, 1 / 255.0, (myDNNsize, myDNNsize), swapRB=True, crop=False)
        net.setInput(blob)
        
        # most CPU intensive part! processing image with DNN
        layerOutputs = net.forward(ln)
        
        # initialize our lists of detected bounding boxes, confidences, and class IDs, respectively
        boxes = []
        confidences = []
        classIDs = []

        # loop over each of the layer outputs
        for output in layerOutputs:
            # loop over each of the detections
            for detection in output:
                # extract the class ID and confidence (i.e., probability) of the current object detection
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
        
        dnnResults = {
            "dino":0.0,
            "frog":0.0,
            "leopard":0.0,
            "turtle":0.0,
            "tomato":0.0,
        }

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
                text = "{}: {:.4f}".format(LABELS[classIDs[i]], confidences[i])
                cv2.putText(frame, text, (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX, 1.3, color, 4)

                dnnResults[LABELS[classIDs[i]]] = confidences[i]
        
        # print(LABELS)
        # print(classIDs)
        # print(confidences)

        return frame, dnnResults