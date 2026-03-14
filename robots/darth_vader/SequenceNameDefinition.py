from .sequences import SEQUENCES

SequenceNameDefinition : dict[str, dict] = {
    "DESLIZA" : {
        "description": "Vader extiende su brazo y lo mueve lentamente de izquierda a derecha",
        "sequence" : SEQUENCES.get("Desliza")
    },
    "MANO" : {
        "description": "Vader le extiende la mano al usuario",
        "sequence" : SEQUENCES.get("Extiende")
    },
    "ADEMAN_1" : {
        "description": "Ademán simple mientras habla 1",
        "sequence" : SEQUENCES.get("Ademan_1")
    },
    "ADEMAN_2" : {
        "description": "Ademán simple mientras habla 2",
        "sequence" : SEQUENCES.get("Ademan_2")
    },
    "PODER" : {
        "description": "Vader flexiona su brazo y aprieta su puño",
        "sequence" : SEQUENCES.get("Poder")
    },
    "DESCANSO" : {
        "description": "Vader posiciona ambos brazos a ambos costados",
        "sequence" : SEQUENCES.get("Descanso")
    },
    "IDLE" : {
        "description" : "No hace nada",
        "sequence" : SEQUENCES.get("Idle")
    },
    "FIN ATACA":{
        "description": "Vader, enciende su sable de luz, ataca y termina con el usuario y la conversación. Sólo se puede usar al final",
        "sequence" : SEQUENCES.get("AttackSequence")
    },
    "FIN ACEPTA":{
        "description" : "Animación de término cuando el usuario acepta",
        "sequence" : SEQUENCES.get("SoundEffect")
    },
    

}


