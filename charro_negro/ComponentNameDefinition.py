from enum import Enum

from ai_talking_robot.sequencer.ComponentEnum import ComponentEnum

class Servos(ComponentEnum):
    # NAME = Channel, (MIN, MAX)
    JAW = (0, 0, 180)
    NECK_X = (1, 0, 180)
    NECK_Y = (2, 0, 180)
    SHOULDER_L_X = (3, 85, 180) #Exterior
    SHOULDER_L_Z = (4, 0, 180) #Interior
    SHOULDER_R_X = (5, 0, 180) #Exterior
    SHOULDER_R_Z = (6, 10, 180) #Interior
    ELBOW_L = (7, 0, 180)
    ELBOW_R = (8, 0, 180)

class Leds(ComponentEnum):
    RIGHT_EYE = (0, 0, 255) 
    LEFT_EYE = (1, 0, 255)

class Audios(ComponentEnum):
    LAUGH = (0, 0, 1)
    BASS = (1, 0, 1)
    CLOSE_CALL = (2, 0, 1)

