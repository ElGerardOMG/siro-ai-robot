from ..ComponentNameDefinition import *

AttackSequence = [
    {
        "parameters":{
            "time" : 1.0,
            "type" : "linear"
        },
        "components":{
            AudioNames.SABER_ON : 1
        }
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
        "parameters":{
            "time" : 2.5,
            "type" : "linear"
        },
        "components":{
            ServoChannelNames.SHOULDER_L_X : 85,
            ServoChannelNames.SHOULDER_L_Z : 0,
            ServoChannelNames.SHOULDER_R_X : 0,
            ServoChannelNames.SHOULDER_R_Z : 10,
            ServoChannelNames.ELBOW_R : 0,
        }
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
