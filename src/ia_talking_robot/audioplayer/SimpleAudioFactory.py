import numpy as np
import simpleaudio as sa
import wave
import io

from pydub import AudioSegment

from .AAudioFactory import AAudioFactory
from .SimpleAudio import SimpleAudio
from .AudioSpec import *

class SimpleAudioFactory(AAudioFactory):

    def create(self, spec):
        if isinstance(spec, Mp3FileSpec):
            audio = AudioSegment.from_file(spec.path, format="mp3")
            audio = self._maybe_reformat(audio, spec.target_sample_rate, spec.target_channels, spec.target_sample_width)
            return SimpleAudio(self._waveobject_from_pydub(audio))

        if isinstance(spec, WavFileSpec):
            if any([spec.sample_rate, spec.channels, spec.sample_width]):
                audio = AudioSegment.from_file(spec.path, format="wav")
                audio = self._maybe_reformat(audio, spec.sample_rate, spec.channels, spec.sample_width)
                return SimpleAudio(self._waveobject_from_pydub(audio))
            return SimpleAudio(sa.WaveObject.from_wave_file(spec.path))

        if isinstance(spec, WavBytesSpec):
            with wave.open(io.BytesIO(spec.data), 'rb') as wav_file:
                return SimpleAudio(sa.WaveObject.from_wave_read(wav_file))

        if isinstance(spec, NumpyArraySpec):  
            audio_data = spec.data
            
            if audio_data.dtype == np.float32:
                audio_data = np.nan_to_num(audio_data, nan=0.0)        # por si hay NaNs
                audio_data = np.clip(audio_data, -1.0, 1.0)
                audio_data = np.rint(audio_data * 32767).astype(np.int16)
            elif audio_data.dtype == np.int16:
                pass
            else:
                raise ValueError(f"Formato no soportado para numpy")

            # Si viene como [samples, channels], convertir a interleaved
            if audio_data.ndim == 2:
                audio_data = audio_data.ravel(order='C')  # interleaved: s0c0, s0c1, s1c0, s1c1...

            audio_data = np.ascontiguousarray(audio_data)

            buf = io.BytesIO()
            with wave.open(buf, 'wb') as f:
                f.setnchannels(spec.channels)
                f.setsampwidth(2)              # 16-bit PCM
                f.setframerate(spec.sample_rate)
                f.writeframes(audio_data.tobytes())
            buf.seek(0)
            with wave.open(buf, 'rb') as wav_file:
                return SimpleAudio(sa.WaveObject.from_wave_read(wav_file))

        
        raise ValueError(f"Spec no soportada: {type(spec).__name__}")

    def _maybe_reformat(self, audio: AudioSegment, sr, ch, sw):
        if sr: audio = audio.set_frame_rate(sr)
        if ch: audio = audio.set_channels(ch)
        if sw: audio = audio.set_sample_width(sw)
        return audio

    def _waveobject_from_pydub(self, audio: AudioSegment):
        buf = io.BytesIO()
        audio.export(buf, format="wav")
        buf.seek(0)
        with wave.open(buf, 'rb') as wav_file:
            return sa.WaveObject.from_wave_read(wav_file)

    