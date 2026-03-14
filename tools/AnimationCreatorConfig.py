from ai_talking_robot.controllers.AComponentController import AComponentController

from ai_talking_robot.controllers.MockController import MockController

from ai_talking_robot.sequencer.DefaultMoveSequencer import DefaultMoveSequencer

from ai_talking_robot.controllers.RemoteUDPController import RemoteUDPController

from .SampleServosDefinition import Servos



def get_config():

    #mockServos = MockController(Servos)
    format = { "servo": "name", "angle": "value" }
    
    virtualServos = RemoteUDPController(Servos, format, "127.0.0.1", 5005)
    sequencer = DefaultMoveSequencer()

    
    return sequencer, Servos