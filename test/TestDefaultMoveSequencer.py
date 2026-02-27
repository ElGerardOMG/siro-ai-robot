import string
from time import sleep

from src.ia_talking_robot.controllers.AComponentController import AComponentController
from src.ia_talking_robot.controllers.AudioPlayerController import AudioPlayerController
from src.ia_talking_robot.controllers.MockController import MockController

from src.ia_talking_robot.sequencer.DefaultMoveSequencer import DefaultMoveSequencer
from src.ia_talking_robot.sequencer.SampleComponentDefinition import *
from src.ia_talking_robot.sequencer.SampleSequence import SampleSequence
from src.ia_talking_robot.sequencer.SampleAudioSequence import SampleAudioSequence
from src.ia_talking_robot.log.ConsoleLogger import ConsoleLogger
    


if __name__ == "__main__":
    logger = ConsoleLogger()
    servoController = MockController(16,"Servo")
    servoController.addNewLogger(logger)
    #ledController = MockController(4,"Led")
    

    sequencer = DefaultMoveSequencer(
        [
            (servoController, Servos),
            

        ]
    )
    print("Ejecutando secuencia normalmente...")
    sequencer.setTimePartionSize(0.2)
    sequencer.executeSequence(SampleSequence)

    
    print("Ejecutando secuencia asíncrona...")
    sequencer.executeSequenceAsync(SampleSequence)
    sleep(2)
    print("Intentando terminar secuencia...")
    sequencer.cancelCurrentSequence()
    
    print("Secuencia terminada")
    print("Ejecutando secuencia asíncrona...")
    sequencer.executeSequenceAsync(SampleSequence)
    sleep(2)
    print("Intentando cambiar el tamaño de los segmentos de tiempo...")
    sequencer.setTimePartionSize(0.1)
    print("Secuencia terminada")
    

   