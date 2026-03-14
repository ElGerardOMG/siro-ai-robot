from ai_talking_robot.audioplayer import AudioSpec
from ai_talking_robot.sequencer.ComponentEnum import ComponentEnum
from ai_talking_robot.controllers.AComponentController import AComponentController
from ai_talking_robot.audioplayer.AAudio import AAudio
from ai_talking_robot.audioplayer.AAudioFactory import AAudioFactory

from ai_talking_robot.audioplayer.AudioSpec import AudioSpec
"""
    Reproductor de Audio adaptado como Component Controller para permitir reproducción de audio en medio
    de las secuencias. Cuando se llama setComponentValue se reproduce el audio de forma asíncrona si es que no 
    está reproduciéndose. El audio también se puede detener si es que se le envía el valor 0.
    Para inicializarlo hace falta que los canales de cada ComponentEnum coincida con los índices de la lista
    de audios.
"""
class AudioPlayerController(AComponentController):

    def __init__(self, components : type[ComponentEnum], audios : list[AAudio]):
        super().__init__(components)
        self._components = components 

        self._audioList = audios 

    def createAudios(self, factory : AAudioFactory, spec : AudioSpec):
        self._audioList = [None] * len(self._components)
        for indx, component in enumerate(self._components):
            if component.label is not None:
                spec.path = component.label
                self._audioList[indx] = factory.create(spec) 

    def setComponentValue(self, component : ComponentEnum, value):
        if value == 0:
            if self._audioList[component.channel].isCurrentlyPlaying():
                self._audioList[component.channel].stop()
        else:
            if not self._audioList[component.channel].isCurrentlyPlaying():
                self._audioList[component.channel].playAudioAsync()
        
    def getComponentValue(self,  component : ComponentEnum):
        return 1 if self._audioList[component.channel].isCurrentlyPlaying() else 0
  
    
    