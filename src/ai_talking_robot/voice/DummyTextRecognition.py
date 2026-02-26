from .ASpeechRecognition import ASpeechRecognition

class DummyTextRecognition(ASpeechRecognition):
   

    def __init__(self):
        pass

    def startRecognition(self) -> str:
        return input("Ingrese su respuesta: ")
        
