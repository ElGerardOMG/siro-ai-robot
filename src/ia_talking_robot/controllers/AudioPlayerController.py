from .AComponentController import AComponentController
from ..audioplayer.AAudio import AAudio

"""
    Reproductor de Audio adaptado como Component Controller para permitir reproducción de audio en medio
    de las secuencias. Cuando se llama setComponentValue se reproduce el audio si es que no está
    reproduciéndose
"""
class AudioPlayerController(AComponentController):

    def __init__(self, audios : list[AAudio]):
        self.audioList = audios
        pass
        
    def setComponentValue(self, component : int, value):
        if 0 <= component < len(self.audioList):
            if value == 0:
                if self.audioList[component].isCurrentlyPlaying():
                    self.audioList[component].stop()
            else:
                if not self.audioList[component].isCurrentlyPlaying():
                    self.audioList[component].playAudioAsync()
        

    def getComponentValue(self, component : int):
        if 0 <= component < len(self.audioList):
            return 1 if self.audioList[component].isCurrentlyPlaying() else 0
        else:
            return 0
    
    