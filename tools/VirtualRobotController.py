import socket
import json
import time
import math
from ai_talking_robot.controllers.AComponentController import AComponentController
from ai_talking_robot.sequencer.ComponentEnum import ComponentEnum

class VirtualRobotController(AComponentController):
    def __init__(self, components: type[ComponentEnum], ip="127.0.0.1", port=5005):
        super().__init__(components)

        self.ip = ip
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        self._components = []
        self._values = {}

        for component in components:
            self._components.append(component)
            self._values.update({component.channel: component.min_value})
            

    def setComponentValue(self, component : ComponentEnum, value):
        
        if value is None:
            return
        
        self._values[component.channel] = value

        payload = {
            "servo": component.name,
            "angle": value
        }
        
        message = json.dumps(payload).encode()
        self.sock.sendto(message, (self.ip, self.port))

    def getComponentValue(self, component: ComponentEnum):
        return self._values[component.channel]

