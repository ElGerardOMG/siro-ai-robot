import string

from ai_talking_robot.controllers.AdafruitServoController import AdafruitServoController
from ai_talking_robot.controllers.AComponentController import AComponentController
from ai_talking_robot.sequencer.DefaultMoveSequencer import DefaultMoveSequencer
from ai_talking_robot.sequencer.SampleComponentDefinition import *
from ai_talking_robot.sequencer.SampleSequence import SampleSequence

        
from ai_talking_robot.controllers.MockController import MockController

if __name__ == "__main__":
    servoController = AdafruitServoController(16)
    ledController = MockController(3,"Led")

    sequencer = DefaultMoveSequencer(
        [
            (servoController, Servos),
            (ledController, Leds)
        ]
    )

    #Modificar esta variable para cambiar la secuencia
    sequence = SampleSequence

    sequencer.executeSequence(sequence)
