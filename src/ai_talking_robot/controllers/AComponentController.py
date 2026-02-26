from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ai_talking_robot.sequencer.ComponentEnum import ComponentEnum

"""
    Clase abstracta que representa un controlador, que implementa alguna lógica
    para accionar o mover componentes, como servos o leds. Recibe un ComponentEnum entero,
    en el que cada miembro debe ser inicializado, pasando como controlador esta clase implementada.

"""

class AComponentController:

    def __init__(self, components : type[ComponentEnum]):
        pass
        
    def setComponentValue(self, component : ComponentEnum, value):
        pass

    def getComponentValue(self,  component : ComponentEnum):
        pass
    
    