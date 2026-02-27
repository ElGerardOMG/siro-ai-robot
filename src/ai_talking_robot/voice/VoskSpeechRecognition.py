from .ASpeechRecognition import ASpeechRecognition

import json
import queue
import time

import sounddevice as sd
from vosk import Model, KaldiRecognizer

import logging

log = logging.getLogger(__name__)
class VoskSpeechRecognition(ASpeechRecognition):
    # Singleton pattern
    _instance = None
    _queue = queue.Queue()

    # Tiempo máximo de silencio antes de cortar (en segundos)
    SILENCE_TIMEOUT = 5.0

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, model: str):
        if not hasattr(self, "_initialized"):
            self._initialized = True
            device_info = sd.query_devices(kind="input")
            self.samplerate = int(device_info["default_samplerate"])
            self.model = Model(model_path=model)

    def _callback(indata, frames, time_info, status):
        if status:
            log.debug(f'Estatus de vosk: {status}')
        VoskSpeechRecognition._queue.put(bytes(indata))

    def startRecognition(self, silence_timeout: float | None = None) -> str:
        """
        Escucha por voz hasta que detecta X segundos de silencio continuo.
        También imprime en el log los partial results.
        """
        if silence_timeout is None:
            silence_timeout = self.SILENCE_TIMEOUT

        # Importante: vaciar la cola antes de empezar,
        # para que ningún fragmento de audio anterior se use en este turno.
        while not self._queue.empty():
            try:
                self._queue.get_nowait()
            except queue.Empty:
                break

        try:
            with sd.RawInputStream(
                samplerate=self.samplerate,
                blocksize=8000,
                device=None,
                dtype="int16",
                channels=1,
                callback=VoskSpeechRecognition._callback,
            ):
                rec = KaldiRecognizer(self.model, self.samplerate)
                last_speech_time = time.time()
                last_partial_text = ""

                while True:
                    try:
                        # Si no llega audio en un tiempo razonable, salimos con lo que tengamos.
                        data = VoskSpeechRecognition._queue.get(timeout=1.0)
                    except queue.Empty:
                        now = time.time()
                        if now - last_speech_time >= silence_timeout:
                            final_result = json.loads(rec.FinalResult())
                            final_text = (
                                final_result.get("text", "") or last_partial_text
                            )
                            log.debug(
                                f"Vosk final por silencio (sin datos): {final_text}"
                            )
                            return final_text
                        continue

                    if rec.AcceptWaveform(data):
                        # Resultado final porque Vosk decidió que terminó la frase
                        result = json.loads(rec.Result())
                        final_text = result.get("text", "") or last_partial_text
                        log.debug(f"Vosk final: {final_text}")
                        return final_text

                    # Si aún no hay resultado final, miramos el parcial
                    partial = json.loads(rec.PartialResult())
                    partial_text = partial.get("partial", "")

                    if partial_text:
                        # Hay algo de voz reconocida, lo mostramos y reiniciamos el contador de silencio
                        log.debug(f"Vosk parcial: {partial_text}")
                        last_partial_text = partial_text
                        last_speech_time = time.time()
                    else:
                        # No hay texto parcial → posible silencio
                        now = time.time()
                        if now - last_speech_time >= silence_timeout:
                            # Demasiado silencio: pedimos el resultado final y cortamos
                            final_result = json.loads(rec.FinalResult())
                            final_text = (
                                final_result.get("text", "") or last_partial_text
                            )
                            log.debug(f"Vosk final por silencio: {final_text}")
                            return final_text

        except Exception:
            log.exception("Error inesperado al reconocer")
            return ""


