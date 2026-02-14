import string

from src.ia_talking_robot.controllers.AdafruitServoController import AdafruitServoController
from src.ia_talking_robot.controllers.AComponentController import AComponentController
from src.ia_talking_robot.sequencer.DefaultMoveSequencer import DefaultMoveSequencer
from src.ia_talking_robot.sequencer.SampleComponentDefinition import *
from src.ia_talking_robot.sequencer.SampleSequence import SampleSequence

        
from src.ia_talking_robot.controllers.MockController import MockController

if __name__ == "__main__":
    servoController = AdafruitServoController(16)
    ledController = MockController(3,"Led")

    sequencer = DefaultMoveSequencer(
        [
            (servoController, ServoChannelNames),
            (ledController, LedChannelNames)
        ]
    )

    #Modificar esta variable para cambiar la secuencia
    sequence = SampleSequence

    sequencer.executeSequence(sequence)
