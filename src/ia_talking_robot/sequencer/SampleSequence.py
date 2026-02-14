from .SampleComponentDefinition import *

SampleSequence = [
    {
        "parameters":{
            "time" : 1.2,
            "type" : "linear"
        },
        "components":{
            ServoChannelNames.SHOULDER_L_X : 85,
            ServoChannelNames.SHOULDER_R_Z : 10,
            ServoChannelNames.SHOULDER_R_X : 0,
            ServoChannelNames.SHOULDER_L_Z : 0,
            ServoChannelNames.ELBOW_R : 0,
        }
    },
    {
        "parameters":{
            "time" : 3.0,
            "type" : "linear"
        },
        "components":{
            ServoChannelNames.SHOULDER_L_X : 180,
            ServoChannelNames.SHOULDER_L_Z : 180,
            ServoChannelNames.SHOULDER_R_X : 180,
            ServoChannelNames.SHOULDER_R_Z : 180,
            ServoChannelNames.ELBOW_R : 180,
        }
    },
    {
        "parameters":{
            "time" : 0.1,
            "type" : "linear"
        },
        "components":{
            LedChannelNames.RIGHT_EYE : 160,
            LedChannelNames.LEFT_EYE : 160,
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
]
