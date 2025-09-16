import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
led  = 26
GPIO.setup(led, GPIO.OUT)
photo_trans = 6
GPIO.setup(photo_trans, GPIO.IN)

while True:
    light  = GPIO.input(photo_trans)
    GPIO.output(led, not(light))
    time.sleep(0.1)