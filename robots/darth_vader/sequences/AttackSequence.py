from ..ComponentNameDefinition import *

AttackSequence = [
  {
        "parameters":{
            "time" : 0.0,
            "type" : "linear"
        },
        "components":{
            AudioNames.SABER_ON : 1
        }
    },

  {
    "parameters" : {
      "time" : 0.5,
      "type" : "linear",
    },
    "components" : {
      Servos.SHOULDER_L_X : 0.0,
      Servos.SHOULDER_L_Z : 90.0,
      Servos.SHOULDER_R_X : 0,
      Servos.SHOULDER_R_Z : 90,
      Servos.ELBOW_L : 60,
      Servos.ELBOW_R : 0,
    },
  },
  {
    "parameters" : {
      "time" : 0.5,
      "type" : "linear",
    },
    "components" : {
      Servos.SHOULDER_L_X : 60,
      Servos.SHOULDER_L_Z : 130,
      Servos.SHOULDER_R_X : 0,
      Servos.SHOULDER_R_Z : 90,
      Servos.ELBOW_L : 60,
      Servos.ELBOW_R : 0,
    },
  },
    {
      "parameters":{
          "time" : 0.0,
          "type" : "linear"
      },
      "components":{
          AudioNames.ATTACK : 1 
      }
  },
  {
    "parameters" : {
      "time" : 0.3,
      "type" : "linear",
    },
    "components" : {
      Servos.SHOULDER_L_X : 0,
      Servos.SHOULDER_L_Z : 150,
      Servos.SHOULDER_R_X : 0,
      Servos.SHOULDER_R_Z : 90,
      Servos.ELBOW_L : 60,
      Servos.ELBOW_R : 0,
    },
  },
  {
    "parameters" : {
      "time" : 1.0,
      "type" : "linear",
    },
    "components" : {
      Servos.SHOULDER_L_X : 0,
      Servos.SHOULDER_L_Z : 90,
      Servos.SHOULDER_R_X : 0,
      Servos.SHOULDER_R_Z : 90,
      Servos.ELBOW_L : 60,
      Servos.ELBOW_R : 0,
    },
  },
    {
      "parameters":{
          "time" : 0.5,
          "type" : "linear"
      },
      "components":{
          AudioNames.SABER_OFF : 1
      }
  },
]