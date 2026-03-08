from ai_talking_robot.controllers.AComponentController import AComponentController

from ai_talking_robot.controllers.MockController import MockController

from ai_talking_robot.sequencer.DefaultMoveSequencer import DefaultMoveSequencer
from .VirtualRobotController import VirtualRobotController

from .SampleServosDefinition import Servos



def get_config():

    #mockServos = MockController(Servos)
    virtualServos = VirtualRobotController(Servos)
    
    sequencer = DefaultMoveSequencer()

    
    return sequencer, Servos