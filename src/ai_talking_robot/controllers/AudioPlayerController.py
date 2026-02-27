from ai_talking_robot.sequencer.ComponentEnum import ComponentEnum
from ai_talking_robot.controllers.AComponentController import AComponentController
from ai_talking_robot.audioplayer.AAudio import AAudio

"""
    Reproductor de Audio adaptado como Component Controller para permitir reproducción de audio en medio
    de las secuencias. Cuando se llama setComponentValue se reproduce el audio de forma asíncrona si es que no 
    está reproduciéndose. El audio también se puede detener si es que se le envía el valor 0.
    Para inicializarlo hace falta que los canales de cada ComponentEnum coincida con los índices de la lista
    de audios.
"""
class AudioPlayerController(AComponentController):

    def __init__(self, components : type[ComponentEnum], audios : list[AAudio]):
        self._components = components 
        self._audioList = audios 

        for component in components:
            component.initialize(self)
            
    def setComponentValue(self, component : ComponentEnum, value):
        if value == 0:
            if self._audioList[component.channel].isCurrentlyPlaying():
                self._audioList[component.channel].stop()
        else:
            if not self._audioList[component.channel].isCurrentlyPlaying():
                self._audioList[component.channel].playAudioAsync()
        
    def getComponentValue(self,  component : ComponentEnum):
        return 1 if self._audioList[component.channel].isCurrentlyPlaying() else 0
  
    
    