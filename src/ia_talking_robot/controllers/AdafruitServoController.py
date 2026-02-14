from enum import Enum
from .AComponentController import AComponentController
#from __future__ import annotations
from adafruit_servokit import ServoKit 

class AdafruitServoController(AComponentController):
    
    def __init__(self, componentCount = 16):
        super().__init__(componentCount)
        self.kit : ServoKit = ServoKit(channels=componentCount)

        self._MOTOR_SWEEP_TIMES = [ 0.800 for _ in range( componentCount ) ]
    
        self.angles = [ 0.0 for _ in range( componentCount )]
     
        
    def _calculate_movement_time(self, angle_diff: float, motor: int) -> float:
        """
        Calculates the time needed to get to the desired angle.
        """

        st = self._MOTOR_SWEEP_TIMES[motor.value]
        return st * angle_diff / 180
        

    def setComponentValue(self, component : int, value):
        if value != None:
            value = round(value)

        self.kit.servo[component].angle = value 

        if value != None:
            self.angles[component] = value


    def getComponentValue(self, component : int):
        return self.angles[component]