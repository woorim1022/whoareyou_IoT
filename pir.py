from threading import Thread
import RPi.GPIO as GPIO
import time


GPIO.setmode(GPIO.BCM)
LED = 21
GPIO.setup(LED, GPIO.OUT) 

class Pir(Thread):
    def __init__(self):
        super().__init__()
        self.value = ""

    def run(self):
        while True:
            GPIO.setmode(GPIO.BCM)
            pirPin = 26
            GPIO.setup(pirPin, GPIO.IN)
            time.sleep(2)
            if GPIO.input(pirPin) == 1:
                self.value = 'on'
                GPIO.output(LED, GPIO.HIGH)
                #print("motion detected")
            else:
                self.value = 'off'
                GPIO.output(LED, GPIO.LOW)
                #print("off")
