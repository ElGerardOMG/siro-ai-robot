import socket
import json
import time
import math
from ai_talking_robot.controllers.AComponentController import AComponentController
from ai_talking_robot.sequencer.ComponentEnum import ComponentEnum


class RemoteUDPController(AComponentController):
    """
    Controlador que envía Jsons a través de UDP. Útil para controlar componentes que estén en otro
    dispositivo y que sea alcanzable por red. Debe ser especificado la dirección ip y el puerto,
    así como también la definición de los campos del json que se envía.
    La definición de los campos es un diccionario que define qué campos se enviarán y con qué nombre.
    Cada valor representa un campo del ComponentEnum
    Los campos disponibles son:
    name, channel, value, max_value, min_value, label

    Si el formato es:
    { "servo": "name",
      "angle": "value" }

    Entonces cuando se llame a setComponentValue, se enviará este formato en json donde "name" será
    reeemplazado por el nombre del componente y "value" por el nuevo valor del componente
    """
    def __init__(self, components: type[ComponentEnum], fields : dict[str, str], ip : str, port : int):
        super().__init__(components)
        
        self.fields = fields
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

        parameters = {
            "name": component.name, 
            "channel": component.channel, 
            "value": value,
            "max_value": component.max_value,
            "min_value": component.min_value,
            "label": component.label
        }

        payload = {field_key: parameters.get(field_value) for field_key, field_value in self.fields.items()}

        message = json.dumps(payload).encode()
        self.sock.sendto(message, (self.ip, self.port))

    def getComponentValue(self, component: ComponentEnum):
        return self._values[component.channel]

