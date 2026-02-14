import soundfile as sf
import io
import simpleaudio as sa
import wave
import numpy as np
from scipy.signal import resample
import time
#import librosa

from misaki import espeak
from misaki.espeak import EspeakG2P

from kokoro_onnx import Kokoro

start_time = 0

def change_pitch(samples, semitone_shift, sample_rate):
    """
    Cambia el pitch del audio reescalando la señal.
    Si se baja el pitch, la duración aumenta; si se sube, la duración disminuye.
    """
    #return librosa.effects.pitch_shift(samples, sr=sample_rate, n_steps=semitone_shift)
    factor = 2.0 ** (semitone_shift / 12.0)  # relación de frecuencia
    new_length = int(len(samples) / factor)
    resampled = resample(samples, new_length)
    return resampled

def add_echo(samples, sample_rate, delay_sec=0.005, decay=0.6):
    """
    Agrega eco con retraso en segundos y decaimiento.
    """
    delay_samples = int(sample_rate * delay_sec)
    output = np.copy(samples)
    if delay_samples < len(samples):
        output[delay_samples:] += samples[:-delay_samples] * decay
    return np.clip(output, -1.0, 1.0)

def overlay_delayed(samples, sample_rate, delay_sec=0.0008):
    """
    Superpone el mismo audio retrasado.
    """
    delay_samples = int(sample_rate * delay_sec)
    delayed = np.zeros_like(samples)
    if delay_samples < len(samples):
        delayed[delay_samples:] = samples[:-delay_samples]
    mixed = samples + delayed
    return np.clip(mixed, -1.0, 1.0)

def play_array(samples, sample_rate=44100):
    """
    Convierte un ndarray[-1.0..1.0] a WaveObject y lo reproduce.
    """
    audio_data = (samples * 32767).astype(np.int16)
    wave_obj = sa.WaveObject(audio_data.tobytes(),
                             num_channels=1,
                             bytes_per_sample=2,
                             sample_rate=sample_rate)
    play_obj = wave_obj.play()
    return play_obj


def startTiming(message : str):
    global start_time
    print(message)
    start_time = time.perf_counter()

def stopTiming():
    end_time = time.perf_counter()
    elapsed_time = end_time - start_time
    print(f"Tiempo transcurrido: {elapsed_time:.6f} segundos\n")


# Misaki G2P with espeak-ng fallback
fallback = espeak.EspeakFallback(british=False)
g2p = EspeakG2P(language="es")


# Kokoro
startTiming("Inicializando Kokoro")
kokoro = Kokoro("resources/models/kokoro/kokoro-v1.0.onnx", "resources/models/kokoro/voices-v1.0.bin")
stopTiming()

# Phonemize
text = "Únete, aún hay tiempo, No te dejes destruir como lo hizo Ohbi guán"
phonemes, _ = g2p(text)


# Create
startTiming("Inferencia")
samples, sample_rate = kokoro.create(phonemes, speed=1.2, voice= "em_alex", lang="es", is_phonemes=True)
stopTiming()


startTiming("Filtros")

# Parámetros configurables
pitch_semitones = -4     # ~ -12%
echo_delay = 0.008       # 5 ms
echo_decay = 0.6
overlay_delay = 0.01   # 0.8 ms

# Aplicar filtros
processed = change_pitch(samples, pitch_semitones, sample_rate)
processed = add_echo(processed, sample_rate, delay_sec=echo_delay, decay=echo_decay)
processed = overlay_delayed(processed, sample_rate, delay_sec=overlay_delay)

stopTiming()


# Save
startTiming("Transformación")

audio_data = (processed * 32767).astype(np.int16)
wave_obj = sa.WaveObject(audio_data.tobytes(),
                            num_channels=1,
                            bytes_per_sample=2,
                            sample_rate=sample_rate)

"""                  
buffer = io.BytesIO()
with wave.open(buffer, 'wb') as f:
    f.setnchannels(1)       # Mono
    f.setsampwidth(2)       # 16 bits
    f.setframerate(sample_rate)   # Frecuencia de muestreo estándar
    f.writeframes(audio_data.tobytes())
buffer.seek(0)
wave_obj = sa.WaveObject.from_wave_read(wave.open(buffer, 'rb'))
"""

startTiming("Reproducción")
obj = wave_obj.play()
obj.wait_done()
stopTiming()

print("Finalización")


