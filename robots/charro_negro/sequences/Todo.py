from ..ComponentNameDefinition import *

Todo = [
  {
    "parameters" : {
      "time" : 1.0,
      "type" : "linear",
    },
    "components" : {
      Servos.NECK_X : 0,
      Servos.NECK_Y : 0,
      Servos.SHOULDER_L_X : 80,
      Servos.SHOULDER_L_Z : 100,
      Servos.SHOULDER_R_X : 80,
      Servos.SHOULDER_R_Z : 100,
      Servos.ELBOW_L : 40,
      Servos.ELBOW_R : 40,
    },
  },
  {
    "parameters" : {
      "time" : 1.0,
      "type" : "linear",
    },
    "components" : {
      Servos.NECK_X : 0,
      Servos.SHOULDER_L_X : 0,
      Servos.SHOULDER_L_Z : 90,
      Servos.SHOULDER_R_X : 0,
      Servos.SHOULDER_R_Z : 90,
      Servos.ELBOW_L : 0,
      Servos.ELBOW_R : 0,
    },
  },
]