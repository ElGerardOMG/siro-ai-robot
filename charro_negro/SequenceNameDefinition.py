
#from charro_negro.sequences import FinAceptFinAcepta, FinRechaza
from .sequences import *

SequenceNameDefinition : dict[str, dict] = {
    "DESLIZA" : {
        "description": "El Charro extiende su brazo y lo mueve lentamente de izquierda a derecha",
        "sequence" : TestSequence
    },
    "MANO" : {
        "description": "El Charro le extiende la mano al usuario",
        "sequence" : TestSequence
    },
    "PRESENTA" : {
        "description": "El Charro coloca su mano en el pecho, señalándose",
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
    "TODO" : {
        "description": "Charro extiende sus brazos a los lados",
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
    "FIN ACEPTA":{
        "description" : "Animación de término cuando el usuario acepta",
        "sequence" : FinAcepta
    },
    "FIN RECHAZA":{
        "description" : "Animación de término cuando el usuario rechaza",
        "sequence" : FinRechaza
    },
    "FIN CANCELA":{
        "description" : "Animación de término cuando el usuario no elige",
        "sequence" : FinRechaza
    }
    
}


