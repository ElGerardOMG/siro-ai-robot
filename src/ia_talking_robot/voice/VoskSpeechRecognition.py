from .ASpeechRecognition import ASpeechRecognition

import json
import queue
import sounddevice as sd
from vosk import Model, KaldiRecognizer

class VoskSpeechRecognition(ASpeechRecognition):
    # Singleton pattern
    _instance = None 
    _queue = queue.Queue()

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, model : str):
        if not hasattr(self, '_initialized'): 
            self._initialized = True
            device_info = sd.query_devices(kind="input")
            self.samplerate = int(device_info["default_samplerate"])
            self.model = Model(model_path=model)


    def _callback(indata, frames, time, status):
        if status:
            print(status)
        VoskSpeechRecognition._queue.put(bytes(indata))


    def startRecognition(self) -> str:
        try:
            with sd.RawInputStream(samplerate=self.samplerate, blocksize = 8000, device=None,
                dtype="int16", channels=1, callback=VoskSpeechRecognition._callback):
                rec = KaldiRecognizer(self.model, self.samplerate)
                while True:
                    data = VoskSpeechRecognition._queue.get()
                    if rec.AcceptWaveform(data):
                        result = rec.Result()
                        resultObject = json.loads(result)
                        return resultObject["text"]
        except Exception as e:
            print(f"Error inesperado: {e}")
            pass


