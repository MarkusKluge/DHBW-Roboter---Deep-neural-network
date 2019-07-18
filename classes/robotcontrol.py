import threading, time, psutil
import RPi.GPIO as GPIO

class RobotControl:
    def __init__(self, diagnostics=None, liveview=None, dnn=None):
        self.diagnostics = diagnostics
        self.liveview = liveview
        self.dnn = dnn
        self.distance = -1

        self.data = {
            'animal': ""
        }

        # self.initDistanceSensor()
        self.runRobotControlThread()
        # self.runDistanceThread()
        print("RobotControl started.")

    def initDistanceSensor(self):
        #GPIO Modus (BOARD / BCM)
        GPIO.setmode(GPIO.BCM)
        
        #GPIO Pins zuweisen
        self.GPIO_DISTANCE_TRIGGER = 23
        self.GPIO_DISTANCE_ECHO = 24
        
        #Richtung der GPIO-Pins festlegen (IN / OUT)
        GPIO.setup(self.GPIO_DISTANCE_TRIGGER, GPIO.OUT)
        GPIO.setup(self.GPIO_DISTANCE_ECHO, GPIO.IN)

    def runRobotControlThread(self):
        x = threading.Thread(target=self.processDNN)
        x.start()

    def runDistanceThread(self):
        x = threading.Thread(target=self.setDistance)
        x.start()
        
    def processDNN(self):
        while True:
            image = self.liveview.getImageRaw()
            if image is not None:
                frame, dnnResults = self.dnn.processImageWithDNN(image)
                self.liveview.setImageDNN(frame, dnnResults)
                # time.sleep(0.1)
                time.sleep(0.25)
                # time.sleep(0.5)
                # time.sleep(1)
                # time.sleep(2)
    # def getData(self):
    #     return self.data
    
    def getDistance(self):
        return self.distance

    def setDistance(self):
        while True:
            print("----------------------------")
            # Wartezeit, um sicher zu gehen, dass der Sensor bereit ist
            GPIO.output(self.GPIO_DISTANCE_TRIGGER, False)
            time.sleep(0.02)

            # setze Trigger auf HIGH
            GPIO.output(self.GPIO_DISTANCE_TRIGGER, True)
        
            # setze Trigger nach 0.01ms aus LOW
            time.sleep(0.00001)
            GPIO.output(self.GPIO_DISTANCE_TRIGGER, False)
            
            StartZeit = time.time()
            # Limitiere die max. Anzahl an while-Schleifendurchgänge, verhindert dass durch ein fehlendes Signal der Prozess sehr lange hängen bleibt
            counter = 0

            # speichere Startzeit
            while GPIO.input(self.GPIO_DISTANCE_ECHO) == 0 and counter <= 1000:
                counter += 1
                pass
            
            if(counter > 1000):
                time.sleep(0.5)
                continue
            StartZeit = time.time()
            
            # speichere Ankunftszeit
            while GPIO.input(self.GPIO_DISTANCE_ECHO) == 1:
                pass
            StopZeit = time.time()
            
            # Zeit Differenz zwischen Start und Ankunft
            TimeElapsed = StopZeit - StartZeit
            # mit der Schallgeschwindigkeit (34320 cm/s) multiplizieren
            # und durch 2 teilen, da hin und zurueck
            distance = (TimeElapsed * 34320) / 2
            self.distance = distance
            print(distance)
            time.sleep(0.5)