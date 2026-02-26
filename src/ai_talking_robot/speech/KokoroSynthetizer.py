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
        self.kokoro = Kokoro(onnxFilePath, voicesBinPath)
        self.g2p = None

        self.voice = None
        self.lang = None
        self.speed = None
        
        self.audio : AAudio = None

    def synthetize(self, text: str):
        self.audio = None
        try:
            phonemes, _ = self.g2p(text)
            samples, sample_rate = self.kokoro.create(
                phonemes, 
                speed=self.speed, 
                voice=self.voice, 
                lang=self.lang, 
                is_phonemes=True
            )
            return self.audioFactory.create(NumpyArraySpec(data=samples, sample_rate=sample_rate))
        except Exception as e:
            raise ValueError(f"Error: {e.with_traceback}")
            
    def getAudio(self):
        """
        Devuelve el último audio sintetizado.
        """
        return self.audio
        
    def setConfig(self, voice : str, language : str = "es", speed : float = 1.0):
        fallback = espeak.EspeakFallback(british=False)

        if language == "en":
            self.g2p = en.G2P(trf=False, british=False, fallback=fallback)
        else:
            self.g2p = EspeakG2P(language=language)
        
        self.voice = voice
        self.lang = language
        self.speed = speed
        