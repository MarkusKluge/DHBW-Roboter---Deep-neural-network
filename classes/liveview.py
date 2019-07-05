import threading, time
import numpy as np
import cv2,base64,imutils

class LiveView:
    def __init__(self, width=1280, height=720, fps=30 ):
        self.width = width
        self.height = height
        self.fps = fps

        self.imageRaw = None
        self.imageJpeg = None
        self.imageDNN = None
        self.dnnResults = None
        
        self.vs = cv2.VideoCapture(0)
        self.vs.set(cv2.CAP_PROP_FRAME_WIDTH, width)
        self.vs.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
        self.vs.set(cv2.CAP_PROP_FPS, 30)
        
        self.runLiveViewThread()
        print("LiveView is running...")

    def runLiveViewThread(self):
        x = threading.Thread(target=self.runLiveView)
        x.start()

    def runLiveView(self):
        while True:
            # for x in range(6):
            for x in range(6):
                (grabbed, frame) = self.vs.read()

            if grabbed:
                self.setImage(frame)
    
    def getImageRaw(self):
        return self.imageRaw

    def getImageJpeg(self):
        return self.imageJpeg

    def setImage(self, frame):
        self.imageRaw = frame
        self.imageJpeg = self.convertToJpeg(frame)

    def setImageDNN(self, frame, dnnResults):
        self.imageDNN = frame

    def getImageDNN(self):
        return self.imageDNN

    def convertToJpeg(self, frame):
        # Convert to jpeg for webview
        ret, image = cv2.imencode('.jpg',frame)
        jpeg = base64.b64encode(image)
        return jpeg
