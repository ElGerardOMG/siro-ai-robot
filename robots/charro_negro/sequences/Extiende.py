from ..ComponentNameDefinition import *

Extiende = [
  {
    "parameters" : {
      "time" : 1.0,
      "type" : "linear",
    },
    "components" : {
      Servos.NECK_X : 0,
      Servos.NECK_Y : 0,
      Servos.SHOULDER_L_X : 0.0,
      Servos.SHOULDER_L_Z : 90.0,
      Servos.SHOULDER_R_X : 0,
      Servos.SHOULDER_R_Z : 130,
      Servos.ELBOW_L : 0.0,
      Servos.ELBOW_R : 50,
    },
  },
  {
    "parameters" : {
      "time" : 0.8,
      "type" : "linear",
    },
    "components" : {
      Servos.SHOULDER_R_X : 0,
      Servos.SHOULDER_R_Z : 150,
      Servos.ELBOW_R : 30.0,
    },
  },
  {
    "parameters" : {
      "time" : 1.5000000000000004,
      "type" : "linear",
    },
    "components" : {
    },
  },
]