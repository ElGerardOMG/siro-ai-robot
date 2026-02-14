from typing import List
import RPi.GPIO as GPIO

from .AComponentController import AComponentController # pyright: ignore

class LedController(AComponentController):

    def __init__(self, componentCount : int, pinList : List[int]):
        super().__init__(componentCount)
        self.pinList = pinList
        self.ledStates = [0 for _ in range(componentCount)]
        self._setpinMode()
        for pin in self.pinList:
            GPIO.setup(pin, GPIO.OUT)
            GPIO.output(pin, GPIO.LOW)

    def _setpinMode(self):
        if GPIO.getmode() is None:
            GPIO.setmode(GPIO.BCM)
            
    def setComponentValue(self, component : int, value):
        if 0 <= component < len(self.pinList):
            pin = self.pinList[component]
            if round(value):
                GPIO.output(pin, GPIO.HIGH)
                self.ledStates[component] = 1
            else:
                GPIO.output(pin, GPIO.LOW)
                self.ledStates[component] = 0

    def getComponentValue(self, component : int):
        if 0 <= component < len(self.ledStates):
            return self.ledStates[component]
        else:
            return None