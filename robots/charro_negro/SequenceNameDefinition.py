from .sequences import SEQUENCES

SequenceNameDefinition : dict[str, dict] = {
    "DESLIZA" : {
        "description": "El Charro extiende su brazo y lo mueve lentamente de izquierda a derecha",
        "sequence" : SEQUENCES.get("Desliza")
    },
    "MANO" : {
        "description": "El Charro le extiende la mano al usuario",
        "sequence" : SEQUENCES.get("Extiende")
    },
    "PRESENTA" : {
        "description": "El Charro Señala rápidamente de frente al usuario",
        "sequence" : SEQUENCES.get("Seniala")
    },
    "ADEMAN_1" : {
        "description": "Ademán simple mientras habla 1",
        "sequence" : SEQUENCES.get("Ademan_1")
    },
    "ADEMAN_2" : {
        "description": "Ademán simple mientras habla 2",
        "sequence" : SEQUENCES.get("Ademan_2")
    },
    "TODO" : {
        "description": "Charro extiende sus brazos a los lados",
        "sequence" : SEQUENCES.get("Todo")
    },
    "DESCANSO" : {
        "description": "Vader posiciona ambos brazos a ambos costados",
        "sequence" : SEQUENCES.get("Descanso")
    },
    "IDLE" : {
        "description" : "No hace nada",
        "sequence" : SEQUENCES.get("Idle")
    },
    "FIN ACEPTA":{
        "description" : "Animación de término cuando el usuario acepta",
        "sequence" : SEQUENCES.get("FinAcepta")
    },
    "FIN RECHAZA":{
        "description" : "Animación de término cuando el usuario rechaza",
        "sequence" : SEQUENCES.get("FinRechaza")
    },
    "FIN CANCELA":{
        "description" : "Animación de término cuando el usuario no elige",
        "sequence" : SEQUENCES.get("FinRechaza")
    }
    

}


