from ai_talking_robot.controllers.AComponentController import AComponentController

from ai_talking_robot.controllers.MockController import MockController

from ai_talking_robot.sequencer.SampleComponentDefinition import *
from ai_talking_robot.sequencer.DefaultMoveSequencer import DefaultMoveSequencer
from .VirtualRobotController import VirtualRobotController




def get_config():

    #mockServos = MockController(Servos)
    virtualServos = VirtualRobotController(Servos)
    mockleds = MockController(Leds)
    
    sequencer = DefaultMoveSequencer()

    
    return sequencer, Servos, Leds