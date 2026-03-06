
from ai_talking_robot.controllers.AComponentController import AComponentController
from ai_talking_robot.sequencer.ComponentEnum import ComponentEnum

from serial import Serial

import logging

log = logging.getLogger(__name__)

class ArduinoSerialController(AComponentController):
    
    """
    Controller used to send messages to the Arduino to control the components via Serial. 
    You must implement the logic to receive these messages and act accordingly in the Arduino 
    yourself. 

    The string 'format' defines how messages will be send when calling setComponentValue and
    what information from the component involved will be included.
    The availible fields are:
    name, channel, value, max_value, min_value, label

    example format: "{channel},{value}"
    If the component's channel is 3 and its new value will be 50, then the message sent to the
    Arduino will look like this: "3,50"

    A serial can be easily initialized like this:
    serial = Serial(arduinoPort, baud_rate, timeout=timeout )
    """
    def __init__(self, components : type[ComponentEnum], serial : Serial, format : str):
        super(AComponentController).__init__(components)

        self._components = components

        self._format = format
        self._serial = serial
        self._values = []

        for indx, component in enumerate(components):
            self._values.append(component.min_value)
            component.label = indx
            

    def setComponentValue(self, component: ComponentEnum, value):
        if value is not None:
            value = max(component.min_value, min(value, component.max_value))
            
            parameters = self._format.format({
                "name": component.name, 
                "channel": component.channel, 
                "value": value,
                "max_value":component.max_value,
                "min_value":component.min_value,
                "label": component.label
            })

            line = self._format.format(**parameters)

            self.serial.write(bytes(line + '\n', 'utf-8'))

            log.debug(f'Enviando al arduino: {line}')

            self._values[component.label] = value

    def getComponentValue(self, component: ComponentEnum):
        return self._values[component.label]


