from ..log.CLoggableObject import CLoggableObject
from .AComponentController import AComponentController

"""
    Mock controller que no hace nada, no está ligado a un componente real.
    Su uso es meramente para pruebas en entornos o sistemas diferentes a la
    Raspberry PI
"""
class MockController(AComponentController, CLoggableObject):
    def __init__(self, componentCount : int, name : str = "component"):
        CLoggableObject.__init__(self)
        self.name = name
        self.values = [0 for _ in range(componentCount)]
        pass
        
    def setComponentValue(self, component : int, value):
        if value is not None:
            value = round(value)
        
        self.values[component] = value
        self.LOG(f"Called {self.name}:[{component}]:{value}")
        pass

    def getComponentValue(self, component : int):
        return self.values[component]