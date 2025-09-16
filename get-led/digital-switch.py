import time
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
led = 26
GPIO.setup(led, GPIO.OUT)
key  = 13
GPIO.setup(key, GPIO.IN)
state = 0


while True:
    if GPIO.input(key):
        state = not(state)
        GPIO.output(led, state)
        time.sleep(0.2)