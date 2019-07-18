from pynput import keyboard
import RPi.GPIO as GPIO
import time

GPIO.cleanup()

motors = [
    {"EN": 16, "IN_1": 20, "IN_2":21},
    {"EN": 6, "IN_1": 13, "IN_2":26},
    {"EN": 25, "IN_1": 23, "IN_2":24}
]
# {"EN": 17, "IN_1": 27, "IN_2":22},

GPIO.setmode(GPIO.BCM)

for index in range(len(motors)):
    print("Initialized Motor"+str(index))
    GPIO.setup(motors[index]["EN"],GPIO.OUT,initial=GPIO.HIGH)
    GPIO.setup(motors[index]["IN_1"],GPIO.OUT,initial=GPIO.LOW)
    GPIO.setup(motors[index]["IN_2"],GPIO.OUT,initial=GPIO.LOW)
    #Set the PWM pin and frequency is 2000hz
    motors[index]["PWM"] = GPIO.PWM(motors[index]["EN"], 1000)
    motors[index]["PWM"].start(0)

def run(delaytime, motorIndex, powerInPercent=100):
    print("Motor"+str(motorIndex)+" run")
    motor = motors[motorIndex]
    GPIO.output(motor["IN_1"], GPIO.HIGH)
    GPIO.output(motor["IN_2"], GPIO.LOW)
    motor["PWM"].ChangeDutyCycle(powerInPercent)
    # time.sleep(delaytime)
    # motor["PWM"].ChangeDutyCycle(0)

def back(delaytime, motorIndex, powerInPercent=100):
    print("Motor"+str(motorIndex)+" back")
    motor = motors[motorIndex]
    GPIO.output(motor["IN_1"], GPIO.LOW)
    GPIO.output(motor["IN_2"], GPIO.HIGH)
    motor["PWM"].ChangeDutyCycle(powerInPercent)
    # time.sleep(delaytime)
    # motor["PWM"].ChangeDutyCycle(0)

def stop():
    for index in range(len(motors)):
        motors[index]["PWM"].ChangeDutyCycle(0)

#Delay 2s	
time.sleep(0.5)

# The key combination to check
COMBINATIONS = [
    {keyboard.Key.shift, keyboard.KeyCode(char='c')},
    {keyboard.Key.shift, keyboard.KeyCode(char='a')},
    {keyboard.Key.shift, keyboard.KeyCode(char='d')},
    {keyboard.Key.shift, keyboard.KeyCode(char='w')},
    {keyboard.Key.shift, keyboard.KeyCode(char='s')},
    {keyboard.Key.shift, keyboard.KeyCode(char='q')},
    {keyboard.Key.shift, keyboard.KeyCode(char='e')}
]

def execute():
    print ("Do Something")

def on_press(key):
    delaytime = 0.01
    # delaytime = 0.025
    # delaytime = 0.5
    # delaytime = 1
    # delaytime = 15

    if any([key in COMBO for COMBO in COMBINATIONS]):
        print("on press: "+str(key))
        if key.char is "a":
            run(delaytime, 0)
        elif key.char is "d":
            back(delaytime, 0)
        elif key.char is "w":
            back(delaytime, 1)
        elif key.char is "s":
            run(delaytime, 1)
        elif key.char is "q":
            run(delaytime, 2)
        elif key.char is "e":
            back(delaytime, 2)
        elif key.char is "c":
            print("Cleanup")
            GPIO.cleanup()
            exit()

def on_release(key):
    if any([key in COMBO for COMBO in COMBINATIONS]):
        stop()
    # pass

with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
    print("listening...")
    listener.join()
