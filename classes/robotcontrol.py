import threading, time, psutil
import RPi.GPIO as GPIO
import statistics
import config as cfg

class RobotControl:
    def __init__(self, diagnostics=None, liveview=None, dnn=None):
        self.motorControlAllowed = True
        self.diagnostics = diagnostics
        self.liveview = liveview
        self.dnn = dnn
        self.distance = -1
        self.animal = ''

        self.heights = cfg.heights.copy()

        self.motorInAndOut = 0
        self.motorUpAndDown = 1
        self.motorCatchAnimal = 2

        self.motors = cfg.motors

        self.initSensors()

        # DNN Thread nur für Debugging
        self.runDnnThread()

        self.runDistanceThread()
        print("RobotControl started.")

    def initSensors(self):
        GPIO.cleanup()

        #GPIO Modus (BOARD / BCM)
        GPIO.setmode(GPIO.BCM)

        #Richtung der GPIO-Pins festlegen (IN / OUT)
        GPIO.setup(cfg.gpios['DISTANCE_TRIGGER'], GPIO.OUT)
        GPIO.setup(cfg.gpios['DISTANCE_ECHO'], GPIO.IN)

        for index in range(len(self.motors)):
            print("Initialized Motor"+str(index))
            GPIO.setup(self.motors[index]["EN"],GPIO.OUT,initial=GPIO.HIGH)
            GPIO.setup(self.motors[index]["IN_1"],GPIO.OUT,initial=GPIO.LOW)
            GPIO.setup(self.motors[index]["IN_2"],GPIO.OUT,initial=GPIO.LOW)
            #Set the PWM pin and frequency is 2000hz
            self.motors[index]["PWM"] = GPIO.PWM(self.motors[index]["EN"], 1000)
            self.motors[index]["PWM"].start(0)

    def searchAnimal(self, animal):
        if animal is not '':
            self.animal = animal
            x = threading.Thread(target=self.searchAnimalThread)
            x.start()

    def test(self):

        self.moveIn(1.1)
        time.sleep(0.2)

        self.moveRopeIn(0.5)
        time.sleep(0.2)
        self.moveRopeIn(0.5)
        time.sleep(0.2)
        self.moveRopeIn(0.5)
        time.sleep(0.2)
        self.moveRopeIn(0.8)
        time.sleep(0.2)

        self.moveOut(0.5)
        self.moveRopeIn(0.5)
        time.sleep(0.2)
        self.moveOut(0.5)

        while self.distance > cfg.finishHeight and self.motorControlAllowed:
            status = "moveDown, cur height: "+str(self.distance)+" next stop: "+str(cfg.finishHeight)
            self.setDiagnosticsStatus(status)
            self.moveDown(0.05)

        self.moveRopeOut(1.0, 85)

        time.sleep(0.2)
        self.moveOut(0.8)
        self.moveRopeOut(0.5)
        self.moveUp(3)

    def searchAnimalThread(self):
        self.heights = cfg.heights.copy()
        self.resetDiagnosticsData()

        status = ("Search animal started ..... : "+self.animal)
        self.setDiagnosticsStatus(status)

        self.motorControlAllowed = True

        print("Heights left:")
        print(self.heights)

        while self.heights:
            nextStop = self.heights.pop(0)
            
            if self.distance < nextStop and self.motorControlAllowed:
                continue

            status = "Move to next height: "+str(nextStop)+"cm."
            self.setDiagnosticsStatus(status)

            while self.distance > nextStop and self.motorControlAllowed:
                status = "moveDown, cur height: "+str(self.distance)+" next stop: "+str(nextStop)
                self.setDiagnosticsStatus(status)

                self.moveDown(0.05)
            self.stop()
            while self.distance < nextStop and self.motorControlAllowed:
                self.moveUp(0.01)

            time.sleep(1)
            self.processDNNonce()

            print("DNN results:")
            print(self.dnnResults)
            print(self.animal+": "+str(self.dnnResults[self.animal]))
            
            if self.dnnResults[self.animal] >= cfg.animalFoundAccuracy:
                status = "Animal "+self.animal+" found with "+str(self.dnnResults[self.animal])+" accuracy."
                self.setDiagnosticsStatus(status)
                self.diagnostics.animalFound(True)
                self.diagnostics.finished(True)

                self.moveIn(1.1)
                time.sleep(0.2)

                self.moveRopeIn(0.6)
                time.sleep(0.2)
                self.moveRopeIn(0.5)
                time.sleep(0.2)
                self.moveRopeIn(0.5)
                time.sleep(0.2)
                self.moveRopeIn(0.8)
                time.sleep(0.2)

                self.moveOut(0.5)
                self.moveRopeIn(0.5)
                time.sleep(0.2)
                self.moveOut(0.5)

                while self.distance > cfg.finishHeight and self.motorControlAllowed:
                    status = "moveDown, cur height: "+str(self.distance)+" next stop: "+str(cfg.finishHeight)
                    self.setDiagnosticsStatus(status)
                    self.moveDown(0.05)

                self.moveRopeOut(1.0, 95)

                time.sleep(0.2)
                self.moveOut(0.8)
                self.moveRopeOut(0.5)
                if self.motorControlAllowed:
                    self.moveUp(3)
                self.moveOut(0.8)
                self.moveRopeOut(0.5)
                break

            # time.sleep(2)
        else:
            print("No stops left.")
            self.stop()
            self.diagnostics.animalFound(False)
            self.diagnostics.finished(True)

    def setDiagnosticsStatus(self, text):
        print(text)
        self.diagnostics.setStatus(text)

    def resetDiagnosticsData(self):
        self.diagnostics.setStatus('')
        self.diagnostics.animalFound(False)
        self.diagnostics.finished(False)

    def moveDown(self, delaytime, powerInPercent=100):
        if self.motorControlAllowed == True:
            motor = self.motors[self.motorUpAndDown]
            GPIO.output(motor["IN_1"], GPIO.HIGH)
            GPIO.output(motor["IN_2"], GPIO.LOW)
            motor["PWM"].ChangeDutyCycle(powerInPercent)
            time.sleep(delaytime)
            motor["PWM"].ChangeDutyCycle(0)

    def moveUp(self, delaytime, powerInPercent=100):
        if self.motorControlAllowed == True:
            motor = self.motors[self.motorUpAndDown]
            GPIO.output(motor["IN_1"], GPIO.LOW)
            GPIO.output(motor["IN_2"], GPIO.HIGH)
            motor["PWM"].ChangeDutyCycle(powerInPercent)
            time.sleep(delaytime)
            motor["PWM"].ChangeDutyCycle(0)

    def moveIn(self, delaytime, powerInPercent=100):
        if self.motorControlAllowed == True:
            status = "moveIn"
            self.setDiagnosticsStatus(status)
            motor = self.motors[self.motorInAndOut]
            GPIO.output(motor["IN_1"], GPIO.HIGH)
            GPIO.output(motor["IN_2"], GPIO.LOW)
            motor["PWM"].ChangeDutyCycle(powerInPercent)
            time.sleep(delaytime)
            motor["PWM"].ChangeDutyCycle(0)

    def moveOut(self, delaytime, powerInPercent=100):
        if self.motorControlAllowed == True:
            status = "moveOut"
            self.setDiagnosticsStatus(status)
            motor = self.motors[self.motorInAndOut]
            GPIO.output(motor["IN_1"], GPIO.LOW)
            GPIO.output(motor["IN_2"], GPIO.HIGH)
            motor["PWM"].ChangeDutyCycle(powerInPercent)
            time.sleep(delaytime)
            motor["PWM"].ChangeDutyCycle(0)

    def moveRopeOut(self, delaytime, powerInPercent=100):
        if self.motorControlAllowed == True:
            status = "moveRopeOut"
            self.setDiagnosticsStatus(status)
            motor = self.motors[self.motorCatchAnimal]
            GPIO.output(motor["IN_1"], GPIO.HIGH)
            GPIO.output(motor["IN_2"], GPIO.LOW)
            motor["PWM"].ChangeDutyCycle(powerInPercent)
            time.sleep(delaytime)
            motor["PWM"].ChangeDutyCycle(0)

    def moveRopeIn(self, delaytime, powerInPercent=100):
        if self.motorControlAllowed == True:
            status = "moveRopeIn"
            self.setDiagnosticsStatus(status)
            motor = self.motors[self.motorCatchAnimal]
            GPIO.output(motor["IN_1"], GPIO.LOW)
            GPIO.output(motor["IN_2"], GPIO.HIGH)
            motor["PWM"].ChangeDutyCycle(powerInPercent)
            time.sleep(delaytime)
            motor["PWM"].ChangeDutyCycle(0)

    def stop(self):
        x = threading.Thread(target=self.stopThread)
        x.start()
    
    def stopThread(self):
        for index in range(len(self.motors)):
            self.motors[index]["PWM"].ChangeDutyCycle(0)
        self.motorControlAllowed = False
        
        status = "Motors stopped. Height: "+str(self.distance)
        self.setDiagnosticsStatus(status)
        time.sleep(1)
        self.motorControlAllowed = True

    def reset(self):
        x = threading.Thread(target=self.resetThread)
        x.start()

    def resetThread(self):
        nextStop = cfg.resetHeight

        for index in range(len(self.motors)):
            self.motors[index]["PWM"].ChangeDutyCycle(0)

        self.moveOut(0.3)
        while self.distance < nextStop and self.motorControlAllowed:
            status = "moveUp, cur height: "+str(self.distance)+" next stop: "+str(nextStop)
            self.setDiagnosticsStatus(status)
            self.moveUp(0.1)
        status = "Motor reseted. Height: "+str(self.distance)
        self.setDiagnosticsStatus(status)
        self.motorControlAllowed = True
        self.resetDiagnosticsData()

    def runDistanceThread(self):
        x = threading.Thread(target=self.setDistance)
        x.start()

    def runDnnThread(self):
        x = threading.Thread(target=self.processDNN)
        x.start()

    def processDNN(self):
        while True:
            image = self.liveview.getImageRaw()
            if image is not None:
                frame, dnnResults = self.dnn.processImageWithDNN(image)
                self.dnnResults = dnnResults
                self.liveview.setImageDNN(frame, dnnResults)
                time.sleep(cfg.sleepProcessDnn)
    def processDNNonce(self):
        image = self.liveview.getImageRaw()
        if image is not None:
            frame, dnnResults = self.dnn.processImageWithDNN(image)
            self.dnnResults = dnnResults
            self.liveview.setImageDNN(frame, dnnResults)

    def getDistance(self):
        return self.distance

    def calcDistance(self):
        # Wartezeit, um sicher zu gehen, dass der Sensor bereit ist
        GPIO.output(cfg.gpios['DISTANCE_TRIGGER'], False)
        time.sleep(0.005)

        # setze Trigger auf HIGH
        GPIO.output(cfg.gpios['DISTANCE_TRIGGER'], True)
    
        # setze Trigger nach 0.01ms aus LOW
        time.sleep(0.00001)
        GPIO.output(cfg.gpios['DISTANCE_TRIGGER'], False)
        
        StartZeit = time.time()
        # Limitiere die max. Anzahl an while-Schleifendurchgänge, verhindert dass durch ein fehlendes Signal der Prozess sehr lange hängen bleibt
        counter = 0
        counter2 = 0

        # speichere Startzeit
        while GPIO.input(cfg.gpios['DISTANCE_ECHO']) == 0 and counter <= 1000:
            counter += 1
            pass
        
        if(counter > 1000):
            return -1
        StartZeit = time.time()
        
        # speichere Ankunftszeit
        while GPIO.input(cfg.gpios['DISTANCE_ECHO']) == 1 and counter2 <= 1000:
            counter2 += 1
            pass
        StopZeit = time.time()

        if(counter2 > 1000):
            return -1
        
        # Zeit Differenz zwischen Start und Ankunft
        TimeElapsed = StopZeit - StartZeit
        # mit der Schallgeschwindigkeit (34320 cm/s) multiplizieren
        # und durch 2 teilen, da hin und zurueck
        distance = (TimeElapsed * 34320) / 2
        return distance

    def setDistance(self):
        while True:
            list = []
            while len(list) < 20:
                distance = self.calcDistance()
                if distance is not -1:
                    list.append(distance)
                    # time.sleep(0.005)
            
            median = statistics.median(list)
            median = round(median,2)
            self.distance = median
            self.diagnostics.setDistance(median)
            # print(self.distance)