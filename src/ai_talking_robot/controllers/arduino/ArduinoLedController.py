from ..AComponentController import AComponentController
from serial import Serial
from ai_talking_robot.sequencer.ComponentEnum import ComponentEnum

import logging

log = logging.getLogger(__name__)

class ArduinoLedController(AComponentController):
    
    def __init__(self, components : type[ComponentEnum], serial : Serial):
    
        self._serial = serial

        self._ledStates = []
     
        for indx, component in enumerate(components):
            component.initialize(self)
            component.label = indx
            self._ledStates.append(component.min_value)

    def setComponentValue(self, component: ComponentEnum, value):
        if value is not None:
            value = max(component.min_value, min(value, component.max_value))
            
            line = f"{component.channel},{value}"

            # This is what is beign sent to the arduino
            self._serial.write(bytes(line + '\n', 'utf-8'))

            log.debug(f'Enviando al arduino: {line}')

            self._ledStates[component.label] = value

    def getComponentValue(self, component: ComponentEnum):
        return self._ledStates[component.label]