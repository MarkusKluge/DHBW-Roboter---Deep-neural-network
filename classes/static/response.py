#Bibliotheken einbinden
import RPi.GPIO as GPIO
import time

#GPIO Modus (BOARD / BCM)
GPIO.setmode(GPIO.BCM)
 
#GPIO Pins zuweisen
GPIO_TRIGGER = 23
GPIO_ECHO = 24
 
#Richtung der GPIO-Pins festlegen (IN / OUT)
GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
GPIO.setup(GPIO_ECHO, GPIO.IN)

def search_animal(animal):
	print(animal)

def distance():
	try:
		distance = getDistance()
		return distance
	except KeyboardInterrupt:
		GPIO.cleanup()

def getDistance():
    # Wartezeit, um sicher zu gehen, dass der Sensor bereit ist
    GPIO.output(GPIO_TRIGGER, False)
    time.sleep(0.02)

    # setze Trigger auf HIGH
    GPIO.output(GPIO_TRIGGER, True)
 
    # setze Trigger nach 0.01ms aus LOW
    time.sleep(0.00001)
    GPIO.output(GPIO_TRIGGER, False)
 
    StartZeit = time.time()
    # Limitiere die max. Anzahl an while-Schleifendurchgänge, verhindert dass durch ein fehlendes Signal der Prozess sehr lange hängen bleibt
    counter = 0

    # speichere Startzeit
    while GPIO.input(GPIO_ECHO) == 0 and counter <= 150:
        counter += 1
        pass

    if(counter > 150):
        return -1
    StartZeit = time.time()

    # speichere Ankunftszeit
    while GPIO.input(GPIO_ECHO) == 1:
        pass
    StopZeit = time.time()
 
    # Zeit Differenz zwischen Start und Ankunft
    TimeElapsed = StopZeit - StartZeit
    # mit der Schallgeschwindigkeit (34320 cm/s) multiplizieren
    # und durch 2 teilen, da hin und zurueck
    distance = (TimeElapsed * 34320) / 2

    print(distance)
    return distance