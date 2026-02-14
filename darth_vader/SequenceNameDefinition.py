
from .sequences import *

SequenceNameDefinition : dict[str, dict] = {
    "ATACAR" : {
        "description": "Vader, enciende su sable de luz, ataca y termina con el usuario y la conversación. Sólo se puede usar al final",
        "sequence" : AttackSequence
    },
    "DESLIZA" : {
        "description": "Vader extiende su brazo y lo mueve lentamente de izquierda a derecha",
        "sequence" : TestSequence
    },
    "MANO" : {
        "description": "Vader le extiende la mano al usuario",
        "sequence" : TestSequence
    },
    "ADEMAN_1" : {
        "description": "Ademán simple mientras habla 1",
        "sequence" : TestSequence
    },
    "ADEMAN_2" : {
        "description": "Ademán simple mientras habla 2",
        "sequence" : TestSequence
    },
    "PODER" : {
        "description": "Vader flexiona su brazo y aprieta su puño",
        "sequence" : TestSequence
    },
    "DESCANSO" : {
        "description": "Vader posiciona ambos brazos a ambos costados",
        "sequence" : TestSequence
    },
    "IDLE" : {
        "description" : "No hace nada",
        "sequence" : TestSequence
    },
    
}


