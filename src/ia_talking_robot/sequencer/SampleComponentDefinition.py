from .ComponentChannelEnum import ComponentChannelEnum

class ServoChannelNames(ComponentChannelEnum):
    # NAME = Channel, (MIN, MAX)
    JAW = 0, (0, 180)
    NECK_X = 1, (0, 180)
    NECK_Y = 2, (0, 180)
    SHOULDER_L_X = 3, (85, 180) #Exterior
    SHOULDER_L_Z = 4, (0, 180) #Interior
    SHOULDER_R_X = 5, (0, 180) #Exterior
    SHOULDER_R_Z = 6, (10, 180) #Interior
    ELBOW_L = 7, (0, 180)
    ELBOW_R = 8, (0, 180)

class LedChannelNames(ComponentChannelEnum):
    RIGHT_EYE = 0, (0, 255) 
    LEFT_EYE = 1, (0, 255)
    LIGHT_SABER = 2, (0, 255)

class AudioNames(ComponentChannelEnum):
    SABER_ON = 0, (0, 1)
    SABER_OFF = 1, (0, 1)
    ATTACK = 2, (0, 1)
