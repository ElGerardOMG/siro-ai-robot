from .ComponentEnum import ComponentEnum
from ..controllers import AComponentController

import time
from typing import Any

import asyncio


#TODO: Este sequencer no considera la velocidad de rotación de los servomotores o de
# movimiento de otros componentes, lo que implica que no es capaz de saber si el 
# componente se movería con éxito a su posición destino antes de que comienze su
# siguiente movimiento.
class DefaultMoveSequencer:

    def __init__(self):
        self.valueUpdateInterval = 0.1
        pass

    def executeSequence(self, sequence : list[dict[str, Any]]):
        for movement in range( len(sequence) ): 
            # Obtener la duración y asegurarse que no sea 0 o menor. La mínima es la duración de la partición.    
            duration = max(self.valueUpdateInterval, sequence[movement]["parameters"]["time"])
            # Calcular la cantidad de segmentos de tiempo
            timeSegments = round(duration / self.valueUpdateInterval)
            # De todos los componentes que se moverán en este paso, tomar 3: Componente, valor actual, valor objetivo
            # Los que su valor objetivo sean None pasarán a ser None de una vez
            values = []
            for k, v in sequence[movement]["components"].items():
                if v is not None:
                    values.append((k, k.currentValue, v))
                else:
                    k.currentValue = None
            # Iniciar un timer
            time_start = time.time()
            # Ejecutar...
            while True:
                # Calcular el tiempo transcurrido
                transcurred = time.time() - time_start
                # Calcular el % (0.0 - 1.0) de tiempo transcurrido
                progress = min(transcurred / duration, 1.0)
                # Por cada tercia de valores
                for component, startValue, targetValue in values:
                    # Calcular el nuevo valor en base al progreso en el tiempo (Interpolación lineal)
                    component.currentValue = startValue + (targetValue - startValue) * progress
                
                # Romper si ya se llegó al 100%
                if progress >= 1.0:
                    break

                time.sleep(self.valueUpdateInterval)

    
  
