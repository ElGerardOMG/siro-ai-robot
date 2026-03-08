from ai_talking_robot.sequencer.ComponentEnum import ComponentEnum

class Servos(ComponentEnum):
    # NAME = (Channel, MIN, MAX)
    NECK_X = (1, 0, 180)
    NECK_Y = (2, 0, 180)
    SHOULDER_L_X = (3, 0, 180) 
    SHOULDER_L_Z = (4, 0, 180) 
    SHOULDER_R_X = (5, 0, 180) 
    SHOULDER_R_Z = (6, 0, 180)
    ELBOW_L = (7, 0, 180)
    ELBOW_R = (8, 0, 180)

