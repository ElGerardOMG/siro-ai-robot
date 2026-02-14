from .AInputActivator import AInputActivator
from ..voice.ASpeechRecognition import ASpeechRecognition

class VoiceRecognitionActivator(AInputActivator):
    
    def __init__(self, recognizer : ASpeechRecognition, activator : str):
        self.recognizer = recognizer
        self.activator = activator.casefold()
        pass

    def waitForInput(self):
        while True:
            result = self.recognizer.startRecognition()
            if result.casefold() == self.activator:
                break