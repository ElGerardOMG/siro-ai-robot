from ..ComponentNameDefinition import *

Seniala = [
  {
    "parameters" : {
      "time" : 0.9,
      "type" : "linear",
    },
    "components" : {
      Servos.NECK_X : 0,
      Servos.NECK_Y : 0,
      Servos.SHOULDER_L_X : 0,
      Servos.SHOULDER_L_Z : 90,
      Servos.SHOULDER_R_X : 0,
      Servos.SHOULDER_R_Z : 155,
      Servos.ELBOW_L : 0,
      Servos.ELBOW_R : 90,
    },
  },
  {
    "parameters" : {
      "time" : 0.40000000000000013,
      "type" : "linear",
    },
    "components" : {
      Servos.NECK_X : 10,
      Servos.SHOULDER_R_X : 0,
      Servos.SHOULDER_R_Z : 155,
      Servos.ELBOW_R : 50,
    },
  },
  {
    "parameters" : {
      "time" : 0.40000000000000013,
      "type" : "linear",
    },
    "components" : {
      Servos.SHOULDER_R_X : 0,
      Servos.SHOULDER_R_Z : 155,
      Servos.ELBOW_R : 90,
    },
  },
]