from ..ComponentNameDefinition import *

Idle = [
  {
    "parameters" : {
      "time" : 1.0,
      "type" : "linear",
    },
    "components" : {
      Servos.NECK_X : 10,
      Servos.NECK_Y : 20,
      Servos.SHOULDER_L_X : 0,
      Servos.SHOULDER_L_Z : 90,
      Servos.SHOULDER_R_X : 0,
      Servos.SHOULDER_R_Z : 90,
      Servos.ELBOW_L : 0,
      Servos.ELBOW_R : 0,
    },
  },
  {
    "parameters" : {
      "time" : 1.0,
      "type" : "linear",
    },
    "components" : {
      Servos.NECK_X : None,
      Servos.NECK_Y : None,
      Servos.SHOULDER_L_X : None,
      Servos.SHOULDER_L_Z : None,
      Servos.SHOULDER_R_X : None,
      Servos.SHOULDER_R_Z : None,
      Servos.ELBOW_L : None,
      Servos.ELBOW_R : None,
    },
  },
]