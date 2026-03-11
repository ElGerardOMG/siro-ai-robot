from .ASpeechRecognition import ASpeechRecognition

class DummyTextRecognition(ASpeechRecognition):
    """
        Dummy voice recognition, instead of regonizing speech to text, it ask user for input.
    """

    def __init__(self):
        pass

    def startRecognition(self) -> str:
        return input("Ingrese su respuesta: ")
        
