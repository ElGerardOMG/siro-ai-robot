from ai_talking_robot.controllers.AComponentController import AComponentController
#from ai_talking_robot.controllers.AdafruitServoController import AdafruitServoController
#from ai_talking_robot.controllers.LedController import LedController
#from ai_talking_robot.controllers.AudioPlayerController import AudioPlayerController
from ai_talking_robot.controllers.MockController import MockController

from ai_talking_robot.sequencer.ComponentEnum import ComponentEnum
from ai_talking_robot.sequencer.SampleComponentDefinition import *
from ai_talking_robot.sequencer.DefaultMoveSequencer import DefaultMoveSequencer
from .VirtualRobotController import VirtualRobotController

def get_config():

    mockServos = MockController(Servos)
    #virtualServos = VirtualRobotController(Servos)
    mockLeds = MockController(Leds)
    
    sequencer = DefaultMoveSequencer()


    return Servos, Leds