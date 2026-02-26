from .ComponentChannelEnum import ComponentChannelEnum


from ..controllers import AComponentController

from time import sleep
from typing import Any
from threading import Thread

#TODO: Este sequencer no considera la velocidad de los servomotores y
# otros componentes, por lo que no es posible calcular el tiempo que tardaría
# en moverse cierto ángulo, ni tampoco estimar el tiempo mínimo de un movimiento
# para evitar que se ejecute el próximo antes de terminar el anterior.
#TODO 2: Algo importante, es que si en una secuencia se manejan componentes que 
# no fueron incluídos al momento de inicializar el DefaultMoveSequencer, esto puede
# causar problemas en los cálculos con valores None, por lo que se debe buscar
# una forma de que al momento de ejecutar una secuencia, se exluyan los componentes
# que no están contemplados o no se tiene su controlador. 
class DefaultMoveSequencer:


    def __init__(self, controllers : list[tuple[AComponentController, ComponentChannelEnum]]):
        self.controllerList = controllers
        self.timePartitionSize = 0.1
        self._executingSequence = False
        self._cancelSignal = False
        pass

    def executeSequence(self, sequence : list[dict[str, Any]]):

        self.waitForSequenceExecution()

        self._executingSequence = True
        self._cancelSignal = False
        # Obtener la lista de enums
        availibleEnums = tuple(t for _, t in self.controllerList)

        for movement in range( len(sequence) ): 
            # Obtener la duración          
            duration = sequence[movement]["parameters"]["time"] 
            # Asegurarse que el tiempo no sea 0 o menor.
            duration = max(self.timePartitionSize, duration)
            # Calcular la cantidad de segmentos de tiempo
            timeSegments = round(duration / self.timePartitionSize)
            # Quitar los componentes con valor None, para evitar problemas en los cálculos
            # y establecer el valor None a esos componentes en ese momento.
            # Además, también, quitar los componentes cuyas Keys no sean reconocidas en la lista de enums
            componentsDict = sequence[movement]["components"]
            componentsFiltered = {k: v for k, v in componentsDict.items() if v is not None and isinstance(k, availibleEnums)}
            componentsNone = [(k, v) for k, v in componentsDict.items() if v is None]
            for k, v in componentsNone:
                self._setComponentValue(k,v) 
            
            # Tomar todos los componentes que se declaran en el paso de la secuencia (Menos los None)...
            components = componentsFiltered.items()
            # contar cuántos son...
            componentCount = len(components)
            # obtener sus "nombres"...
            componentNames = [n[0] for n in components]
            # y también sus valores actuales directamente de los AComponentController's
            currentValues = [self._getComponentValue(c) for c in componentNames]
            # finalmente, del paso de la secuencia, obtener sus valores finales
            endValues = [v[1] for v in components]
            
            # WARNING: Esto sólo funciona con el movimiento linear, es decir con velocidad constante
            # Para movimientos más suaves y menos "robóticos", se requeriría calcular el cambio
            # en cada iteración 

            stepValues = [ (endValues[s] - currentValues[s]) / timeSegments 
                            for s in range( componentCount )]

            for step in range(timeSegments):
                
                for component in range(componentCount):
                    
                    currentValues[component] = currentValues[component] + stepValues[component]
                    self._setComponentValue(componentNames[component], currentValues[component])
                   
                sleep(self.timePartitionSize)
      
                if self._cancelSignal:
                    self._cancelSignal = False
                    self._executingSequence = False
                    return

        self._executingSequence = False
  

    def executeSequenceAsync(self, sequence : list[dict[str, Any]]):
        self.waitForSequenceExecution()
        Thread(target=self.executeSequence, args=(sequence,)).start()

    def setTimePartionSize(self, partitionSize : float):
        self.waitForSequenceExecution()
        self.timePartitionSize = partitionSize


    def isExecutingSequence(self):
        return self._executingSequence

    def cancelCurrentSequence(self):
        if self._executingSequence:
            self._cancelSignal = True
        
    def waitForSequenceExecution(self):
       while self._executingSequence:
            sleep(0.01)
    
    def _getComponentValue(self, componentChannel : ComponentChannelEnum):
        for componentController, componentEnumType in self.controllerList:
            if type(componentChannel) == componentEnumType:
                return componentController.getComponentValue(componentChannel.value())   
                

    def _setComponentValue(self, componentChannel : ComponentChannelEnum, value):
        for controller, componentEnumType in self.controllerList:
            if type(componentChannel) == componentEnumType:
                if value is not None: 
                    value = max(componentChannel.MIN(), min(value, componentChannel.MAX()))
                controller.setComponentValue(componentChannel.value(), value)   
                return