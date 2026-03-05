
from ai_talking_robot.controllers.AComponentController import AComponentController

from ai_talking_robot.sequencer.ComponentEnum import ComponentEnum

from serial import Serial

import logging

log = logging.getLogger(__name__)

class ArduinoServoController(AComponentController):
    
    """
    Controller used for the PCA9685 when its connected over Arduino. This
    controller sends messages to the Arduino Board via serial.
    """

    def __init__(self, components : type[ComponentEnum], serial : Serial):
        self._components = components
        
        self.serial = serial
       
        self._servos = [None for _ in range(len(components))]

        for component in components:
            self._servos[component.channel] = component.min_value
            component.initialize(self)

    def setComponentValue(self, component: ComponentEnum, value):
        if value is not None:
            value = max(component.min_value, min(value, component.max_value))
            
            line = f"{component.channel},{value}"

            self.serial.write(bytes(line + '\n', 'utf-8'))

            log.debug(f'Enviando al arduino: {line}')

            self._servos = value

    def getComponentValue(self, component: ComponentEnum):
        return self._servos[component.channel]

    def _calculate_movement_time(self, angle_diff: float, motor: int) -> float:
        """
        Calculates the time needed to get to the desired angle.
        """

        st = self._MOTOR_SWEEP_TIMES[motor.value]
        return st * angle_diff / 180
        