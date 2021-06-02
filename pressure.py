from threading import Thread
import RPi.GPIO as GPIO
import time


class Pressure(Thread):
    def __init__(self):
        super().__init__()
        self.value = ""

    def run(self):
        GPIO.setmode(GPIO.BCM)
        self.pressurePin = 4
        GPIO.setup(self.pressurePin, GPIO.IN)
        while True:
            time.sleep(2)
            if GPIO.input(self.pressurePin) == 1:
                self.value = 'pressure detected'
                #print("pressure 1")
            else:
                self.value = 'off'
                #print("pressure 0")


pressure = Pressure()
pressure.start()