import threading, time, psutil

class RobotControl:
    def __init__(self, diagnostics, liveview, dnn):
        self.diagnostics = diagnostics
        self.liveview = liveview
        self.dnn = dnn

        self.data = {
            'animal': ""
        }
        
        self.runRobotControlThread()
        print("RobotControl started.")

    def runRobotControlThread(self):
        x = threading.Thread(target=self.processDNN)
        x.start()
        
    def processDNN(self):
        while True:
            image = self.liveview.getImageRaw()
            if image is not None:
                frame, dnnResults = self.dnn.processImageWithDNN(image)
                self.liveview.setImageDNN(frame, dnnResults)
                # time.sleep(0.25)
                time.sleep(0.5)
                # time.sleep(1)
                # time.sleep(2)
    # def getData(self):
    #     return self.data
    