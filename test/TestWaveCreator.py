import numpy as np
from scipy.io.wavfile import write

def generar_onda_seno_float32(frecuencia=440, duracion=3.0, sample_rate=44100, amplitud=0.002, nombre_archivo="onda_seno.wav"):
    t = np.linspace(0, duracion, int(sample_rate * duracion), endpoint=False)
    onda = amplitud * np.sin(2 * np.pi * frecuencia * t)
    onda = onda.astype(np.float32)

    # Convertimos a un formato de 16 bits (PCM) porque los archivos WAV suelen tener este formato.
    # Esto se hace escalando la onda a un rango de -32768 a 32767 (para 16-bit signed PCM)
    onda_int16 = np.int16(onda * 32767)
    
    # Guardamos el archivo WAV
    write(nombre_archivo, sample_rate, onda_int16)
    print(f"Archivo guardado como: {nombre_archivo}")

generar_onda_seno_float32()