from misaki import en, espeak
from misaki.espeak import EspeakG2P
import threading
from kokoro_onnx import Kokoro

from ..audioplayer.AAudioFactory import AAudioFactory
from .AVoiceSynthetizer import AVoiceSynthetizer
from ..log.CLoggableObject import CLoggableObject
from ..audioplayer.AudioSpec import NumpyArraySpec
from ..audioplayer.AAudio import AAudio

class KokoroSynthetizer(AVoiceSynthetizer, CLoggableObject):

    def __init__(self, 
        audioFactory : AAudioFactory, 
        onnxFilePath : str, 
        voicesBinPath : str
    ):
        AVoiceSynthetizer.__init__(self,audioFactory)
        CLoggableObject.__init__(self)
        #kokoro = Kokoro("src/resources/models/kokoro/kokoro-v1.0.onnx", "src/resources/models/kokoro/voices-v1.0.bin")
        self.kokoro = Kokoro(onnxFilePath, voicesBinPath)
        self.g2p = None

        self.voice = None
        self.lang = None
        self.speed = None
        
        self.audio : AAudio = None
        self.synthetizing = False
        pass

    def synthetize(self, text: str):
        """
        Sintetiza el texto de forma síncrona (bloqueante).
        """
        self.synthetizing = True
        self.audio = None
        try:
            self.audio = self._sinthetize(text)
            self.synthetizing = False
            return self.audio
        except Exception as e:
            self.synthetizing = False
            raise ValueError(f"Error: {e.with_traceback}")
            
            

    def synthetizeAsync(self, text: str):
        """
        Sintetiza el texto de forma asíncrona (no bloqueante).
        """
        
        def worker():
            try:
                self.audio = self._sinthetize(text)
            finally:
                self.synthetizing = False

        self.synthetizing = True
        self.audio = None
        hilo = threading.Thread(target=worker)
        hilo.start()
        return None

    def _sinthetize(self, text: str):
        """
        Lógica interna para sintetizar el texto usando Kokoro.
        """
        phonemes, _ = self.g2p(text)
        samples, sample_rate = self.kokoro.create(
            phonemes, 
            speed=self.speed, 
            voice=self.voice, 
            lang=self.lang, 
            is_phonemes=True
        )
        return self.audioFactory.create(NumpyArraySpec(data=samples, sample_rate=sample_rate))


    def getAudio(self):
        while self.synthetizing:
            pass

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
        