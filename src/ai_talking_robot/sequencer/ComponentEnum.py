from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ai_talking_robot.controllers.AComponentController import AComponentController

"""
    ComponentEnum es un enum que representa un componente único (Un servo, un led), aunque en 
    realidad funciona como "Puente" o "Enlace" a un Controller.
    Contiene la información necesaria para que el controller lo maneje, su canal único, 
    su valor máximo y mínimo.
    Debe ser inicializado con algún controlador con initialize().
    A través de su propiedad currentValue es posible accionar a su Controller para que este
    lo mueva o lo accione. Cada miembro ComponentEnum no guarda su propio valor, es el
    Controller el que debe de manejar su valor.
    Una clase que herede de este enum representaría un conjunto de componentes manejados por un
    único controlador.
    Está hecho para facilitar la creación de animaciones (Secuencias de Components) y que el 
    Sequencer no tenga que estar constantemente averiguando a qué componente pertenece cada controlador,
    sino que el propio componente sepa a qué controlador pertenece, así como evitar ligar cada
    componente a un único controlador.
"""
class ComponentEnum(Enum):
    #Syntaxis:
    #COMPONENT_NAME = (channel, min_value, max_value)

    def __init__(self, channel, min_value, max_value):
        self.channel = channel
        self.min_value = min_value
        self.max_value = max_value

        self.label = None
        self._controller : AComponentController = None

    def initialize(self, controller : AComponentController):
        if self._controller is not None:
            raise ValueError("This component has already been initialized!")
        self._controller = controller

    @property
    def currentValue(self):
        return self._controller.getComponentValue(self)

    @currentValue.setter
    def currentValue(self, value):
        self._controller.setComponentValue(self, value)

    def isInitialized(self) -> bool:
        return self._controller is not None