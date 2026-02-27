from misaki import en, espeak
from misaki.espeak import EspeakG2P
from kokoro_onnx import Kokoro

from .AVoiceSynthetizer import AVoiceSynthetizer

from ..audioplayer.AAudioFactory import AAudioFactory
from ..audioplayer.AudioSpec import NumpyArraySpec
from ..audioplayer.AAudio import AAudio

class KokoroSynthetizer(AVoiceSynthetizer):

    def __init__(self, 
        audioFactory : AAudioFactory, 
        onnxFilePath : str, 
        voicesBinPath : str
        ):
        
        AVoiceSynthetizer.__init__(self,audioFactory)
        #kokoro = Kokoro("src/resources/models/kokoro/kokoro-v1.0.onnx", "src/resources/models/kokoro/voices-v1.0.bin")
        self._kokoro = Kokoro(onnxFilePath, voicesBinPath)
        self._g2p = None

        self._voice = None
        self._lang = None
        self._speed = 1.0
        
        self._audio : AAudio = None

    def synthetize(self, text: str) -> AAudio:
        self._audio = None
        try:
            phonemes, _ = self._g2p(text)
            samples, sample_rate = self._kokoro.create(
                phonemes, 
                speed=self._speed, 
                voice=self._voice, 
                lang=self._lang, 
                is_phonemes=True
            )
            self._audio = self.audioFactory.create(NumpyArraySpec(data=samples, sample_rate=sample_rate))
            return self._audio
        except Exception as e:
            raise ValueError(f"Error: {e.with_traceback}")
            
    def getAudio(self):
        """
        Devuelve el último audio sintetizado.
        """
        return self._audio
        
    def setConfig(self, voice : str, language : str = "es", speed : float = 1.0):
        fallback = espeak.EspeakFallback(british=False)

        if language == "en":
            self._g2p = en.G2P(trf=False, british=False, fallback=fallback)
        else:
            self._g2p = EspeakG2P(language=language)
        
        self._voice = voice
        self._lang = language
        self._speed = speed
        