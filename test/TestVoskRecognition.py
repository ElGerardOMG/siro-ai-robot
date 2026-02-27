
from ai_talking_robot.voice.VoskSpeechRecognition import VoskSpeechRecognition
import logging
import sys

if __name__ == "__main__":
    # El modelo es pesado, por lo que se tarda cargándolo.
    log = logging.getLogger()
    log.setLevel(logging.DEBUG)
    log.addHandler(logging.StreamHandler(sys.stdout))
    logging.getLogger("ai_talking_robot.voice.VoskSpeechRecognition").setLevel(logging.DEBUG)

    rec = VoskSpeechRecognition(model="resources/models/vosk-model-es-0.42")
    exit = ""
    while exit != "1":
        print("Comenzando reconocimiento")
        response = rec.startRecognition()
        print(f"Reconocido: {response}")
        exit = input("Digite 1 para salir, 0 para repetir: ")