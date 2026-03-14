from ai_talking_robot.sequencer.ComponentEnum import ComponentEnum
from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent

class Servos(ComponentEnum):
    NECK_X = (1, 0, 180)
    SHOULDER_L_X = (3, 0, 180) #Exterior
    SHOULDER_L_Z = (4, 0, 180) #Interior
    SHOULDER_R_X = (5, 0, 180) #Exterior
    SHOULDER_R_Z = (6, 10, 180) #Interior
    ELBOW_L = (7, 0, 180)
    ELBOW_R = (8, 0, 180)

class Leds(ComponentEnum):
    EYES = (0, 0, 255) 
    LIGHT_SABER = (1, 0, 255)

class AudioNames(ComponentEnum):
    SABER_ON = (0, 0, 1, f"{BASE_DIR}/audios/saber_on.wav")
    SABER_OFF = (1, 0, 1, f"{BASE_DIR}/audios/saber_off.wav")
    ATTACK = (2, 0, 1, f"{BASE_DIR}/audios/attack.wav")
    FINAL = (3, 0, 1, f"{BASE_DIR}/audios/imperial_march.wav")