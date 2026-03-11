import RPi.GPIO as GPIO

from ai_talking_robot.sequencer.ComponentEnum import ComponentEnum
from ai_talking_robot.controllers.AComponentController import AComponentController # pyright: ignore

class LedController(AComponentController):

    """
    Controller used to controll leds when they are connected over the Raspberry PI pins
    The channel propery of the Enum is used as the Pin number. It can be BCM or BOARD.
    However, if gpio mode is already initialized with a different mode, it will raise
    value error.
    """
    def __init__(self, components : type[ComponentEnum], gpio_mode = GPIO.BCM):
        super().__init__(components)
        
        if GPIO.getmode() is not None:
            if GPIO.getmode() != gpio_mode:
                raise ValueError(f"GPIO Mode is already initialized with {GPIO.getMode()}")
        else:
            GPIO.setmode(gpio_mode)

        self._components = components

        self._leds = {}

        for component in components:
            self._leds.update({component.channel : 0})
            GPIO.setup(component.channel, GPIO.OUT)
            GPIO.output(component.channel, GPIO.LOW)
            
    def setComponentValue(self, component: ComponentEnum, value):
        pin = component.channel
        if round(value):
            GPIO.output(pin, GPIO.HIGH)
            self._leds[component.channel] = 1
        else:
            GPIO.output(pin, GPIO.LOW)
            self._leds[component.channel] = 0

    def getComponentValue(self, component: ComponentEnum):
        return self._leds[component.channel]