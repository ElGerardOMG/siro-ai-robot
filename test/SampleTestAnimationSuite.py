from ai_talking_robot.sequencer.ComponentEnum import ComponentEnum

class SampleComponents(ComponentEnum):
    COMPONENTE_A = 0, 0, 180
    COMPONENTE_B = 1, 0, 90
    COMPONENTE_C = 2, 0, 45
    COMPONENTE_D = 3, 0, 255

class SampleComponentsAudios(ComponentEnum):
    AUDIO_1 = 0, 0, 1
    AUDIO_2 = 1, 0, 1
    AUDIO_3 = 2, 0, 1

ANIMACION_1 = [
    {
        "parameters" : {
            "time" : 1.5,
            "type" : "linear",
        },
        "components": {
            SampleComponents.COMPONENTE_A : 180,
            SampleComponents.COMPONENTE_B : 90
        },
    },
    {
        "parameters" : {
            "time" : 1.5,
            "type" : "squared",
        },
        "components": {
            SampleComponents.COMPONENTE_C : 90,
            SampleComponents.COMPONENTE_D : 45
        },
    },
    {
        "parameters" : {
            "time" : 1.5,
            "type" : "squared",
        },
        "components": {
            SampleComponents.COMPONENTE_A : 45,
            SampleComponents.COMPONENTE_C : 10
        },
    }
]

ANIMACION_2 = [
    {
        "parameters" : {
            "time" : 10.0,
            "type" : "linear",
        },
        "components": {
            SampleComponents.COMPONENTE_A : 45,
            SampleComponents.COMPONENTE_B : 45,
            SampleComponents.COMPONENTE_C : 45,
            SampleComponents.COMPONENTE_D : 45
        },
    },
]

ANIMACION_3 = [
    {
        "parameters" : {
            "time" : 3.0,
            "type" : "squared",
        },
        "components": {
            SampleComponents.COMPONENTE_A : 1000,
            SampleComponents.COMPONENTE_B : 1000,
            SampleComponents.COMPONENTE_C : 1000,
            SampleComponents.COMPONENTE_D : 1000,
        },
    },
    {
        "parameters" : {
            "time" : 3.0,
            "type" : "squared",
        },
        "components": {
            SampleComponents.COMPONENTE_A : -1000,
            SampleComponents.COMPONENTE_B : -1000,
            SampleComponents.COMPONENTE_C : -1000,
            SampleComponents.COMPONENTE_D : -1000,
        },
    },
]

FIN_ANIM = [
    {
        "parameters" : {
            "time" : 2.0,
            "type" : "squared",
        },
        "components": {
            SampleComponentsAudios.AUDIO_1: 50,
            SampleComponents.COMPONENTE_A : 50,
            SampleComponents.COMPONENTE_B : 50,
        },
    },
    {
        "parameters" : {
            "time" : 2.0,
            "type" : "squared",
        },
        "components": {
            SampleComponents.COMPONENTE_A : 10,
            SampleComponents.COMPONENTE_B : 10,
        },
    },
    {
        "parameters" : {
            "time" : 2.0,
            "type" : "squared",
        },
        "components": {
            SampleComponentsAudios.AUDIO_2: 1,
            SampleComponents.COMPONENTE_A : 10,
            SampleComponents.COMPONENTE_B : 10,
        },
    },
    {
        "parameters" : {
            "time" : 2.0,
            "type" : "squared",
        },
        "components": {
            SampleComponentsAudios.AUDIO_3: 1,
            SampleComponents.COMPONENTE_A : 30,
            SampleComponents.COMPONENTE_B : 30,
        },
    },
]

SampleTestSequences : dict[str, dict] = {
    "ANIMACION_1" : {
        "description": "Animación 1 regular",
        "sequence" : ANIMACION_1
    },
    "ANIMACION_2" : {
        "description": "Animación que es muy larga en duración",
        "sequence" : ANIMACION_2
    },
    "ANIMACION_3" : {
        "description": "Animación que pone los componentes más de su valor máximo",
        "sequence" : ANIMACION_3
    },
    "FIN" : {
        "description": "Animación que incluye audio",
        "sequence" : FIN_ANIM
    },
}