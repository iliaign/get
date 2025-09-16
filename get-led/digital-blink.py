import RPi.GPIO as GPIO
import time


GPIO.setmode(GPIO.BCM)
led = 26
GPIO.setup(led, GPIO.OUT)
state = 0
period_popolam = 1.0

while True:
    GPIO.output(led, state)
    state = not(state)
    time.sleep(period_popolam)