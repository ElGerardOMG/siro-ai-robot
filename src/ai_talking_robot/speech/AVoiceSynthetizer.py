from ..audioplayer import AAudio

from ..audioplayer.AAudioFactory import AAudioFactory

class AVoiceSynthetizer:

    def __init__(self, audioFactory : AAudioFactory):
        self.audioFactory = audioFactory
        pass

    def synthetize(self, text: str) -> AAudio:
        pass

    def getAudio(self) -> AAudio:
        pass
