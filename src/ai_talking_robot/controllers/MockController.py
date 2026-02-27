import numbers
import logging
#from ..log.CLoggableObject import CLoggableObject
from ai_talking_robot.controllers.AComponentController import AComponentController
from ai_talking_robot.sequencer.ComponentEnum import ComponentEnum



log = logging.getLogger(__name__)

"""
    Mock controller que no hace nada, no está representa un controlador real.
    Su uso es para reemplazar a los controladores reales en caso de que no puedan
    usarse o no se dispongan en entornos de pruebas.
"""
class MockController(AComponentController):
    def __init__(self, components : type[ComponentEnum], name: str = "controller"):
        self.name = name
        self._components = components

        self._values = []
        for index, component in enumerate(components):
            component.initialize(self)
            component.label = index
            self._values.append(component.min_value)
       
        
    def setComponentValue(self, component : ComponentEnum, value):
        if value is not None:
            
            if isinstance(value, numbers.Number):
                value = min(max(value, component.min_value), component.max_value)
                value = round(value)

            self._values[component.label] = value
        
        log.debug(f"Llamado {self.name}:[{component.name}]:{value}")

    def getComponentValue(self, component : ComponentEnum):
        return self._values[component.label]
