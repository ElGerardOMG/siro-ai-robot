
from .AudioSpec import *
import numpy as np
from scipy.signal import resample
from scipy.io import wavfile
import io

from .AAudioFactory import AAudioFactory

"""
    Esta clase es un wrapper para otro AAudioFactory. Antes de crear un audio, le aplica
    ciertos filtros. Por ahora, es simple y los filtros están predeterminados
"""
class AudioFactoryFilter(AAudioFactory):

    def __init__(self, audioFactory : AAudioFactory):
        self._audioFactory = audioFactory
        self.pitch_semitones = -4     # ~ -12%
        self.echo_delay = 0.008       # 5 ms
        self.echo_decay = 0.6
        self.overlay_delay = 0.01   # 0.8 ms
        self.gain = 1.0
        pass

    def create(self, spec: AudioSpec):
        
        if isinstance(spec, NumpyArraySpec):  
            audio_data = spec.data
            
            if audio_data.dtype == np.int16:
                audio_data = audio_data.astype(np.float32) / 32767.0
            elif audio_data.dtype == np.float32:
                audio_data = np.nan_to_num(audio_data, nan=0.0)        
                audio_data = np.clip(audio_data, -1.0, 1.0)
            else:
                raise ValueError(f"Formato no soportado para numpy")

            sample_rate = spec.sample_rate

        elif isinstance(spec, WavBytesSpec):
            # Read the WAV bytes using wavfile.read
            sample_rate, audio_data_original_dtype = wavfile.read(io.BytesIO(spec.data))
            # Convert to float32 and normalize
            audio_data = audio_data_original_dtype.astype(np.float32) / np.iinfo(audio_data_original_dtype.dtype).max
        else:
            raise ValueError(f"{type(spec)} not supported for now...")

        audio_data = _change_pitch(audio_data, self.pitch_semitones)
        audio_data = _add_echo(audio_data, sample_rate, self.echo_delay, self.echo_decay)
        audio_data = _overlay_delayed(audio_data, sample_rate, self.overlay_delay)
        audio_data = _adjust_volume(audio_data, self.gain)
        return self._audioFactory.create(NumpyArraySpec(data=audio_data, sample_rate = sample_rate))
        
        
def _change_pitch(samples, semitone_shift):
    """
    Cambia el pitch del audio reescalando la señal.
    Si se baja el pitch, la duración aumenta; si se sube, la duración disminuye.
    """
    factor = 2.0 ** (semitone_shift / 12.0)  # relación de frecuencia
    new_length = int(len(samples) / factor)
    resampled = resample(samples, new_length)
    return resampled

def _add_echo(samples, sample_rate, delay_sec, decay):
    """
    Agrega eco con retraso en segundos y decaimiento.
    """
    delay_samples = int(sample_rate * delay_sec)
    output = np.copy(samples)
    if delay_samples < len(samples):
        output[delay_samples:] += samples[:-delay_samples] * decay
    return np.clip(output, -1.0, 1.0)

def _overlay_delayed(samples, sample_rate, delay_sec):
    """
    Superpone el mismo audio retrasado.
    """
    delay_samples = int(sample_rate * delay_sec)
    delayed = np.zeros_like(samples)
    if delay_samples < len(samples):
        delayed[delay_samples:] = samples[:-delay_samples]
    mixed = samples + delayed
    return np.clip(mixed, -1.0, 1.0)

def _adjust_volume(samples, gain=1.0):
    amplified = samples * gain
    return np.clip(amplified, -1.0, 1.0)