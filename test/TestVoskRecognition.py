
from ..ia_talking_robot.voice.VoskSpeechRecognition import VoskSpeechRecognition


if __name__ == "__main__":
    # El modelo es pesado, por lo que se tarda cargándolo.
    rec = VoskSpeechRecognition()
    exit = ""
    while exit != "1":
        print("Comenzando reconocimiento")
        response = rec.startRecognition()
        print(f"Reconocido: {response}")
        exit = input("Digite 1 para salir, 0 para repetir: ")