from src.ia_talking_robot.audioplayer import AAudio

from ..audioplayer.AAudioFactory import AAudioFactory

class AVoiceSynthetizer:

    def __init__(self, audioFactory : AAudioFactory):
        self.audioFactory = audioFactory
        pass

    def synthetize(self, texto: str) -> AAudio:
        pass

    def synthetizeAsync(self, text: str):
        pass

    def getAudio(self) -> AAudio:
        pass
