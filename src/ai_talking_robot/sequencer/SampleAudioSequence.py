from .SampleComponentDefinition import *

SampleAudioSequence = [
    {
        "parameters":{
            "time" : 1.2,
            "type" : "linear"
        },
        "components":{
            Servos.SHOULDER_L_X : 85,
            Servos.SHOULDER_R_Z : 10,
            Servos.SHOULDER_R_X : 0,
            Servos.SHOULDER_L_Z : 0,
            Servos.ELBOW_R : 0,
        }
    },
    {
        "parameters":{
            "time" : 0,
            "type" : "linear"
        },
        "components":{
            Audios.ATTACK : 1
        }
    },
    {
        "parameters":{
            "time" : 3.0,
            "type" : "linear"
        },
        "components":{
            Servos.SHOULDER_L_X : 180,
            Servos.SHOULDER_L_Z : 180,
            Servos.SHOULDER_R_X : 180,
            Servos.SHOULDER_R_Z : 180,
            Servos.ELBOW_R : 180,
        }
    },
]