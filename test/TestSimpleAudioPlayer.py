import os
import numpy as np
import wave

from pathlib import Path

from ai_talking_robot.audioplayer.SimpleAudioFactory import SimpleAudioFactory
from ai_talking_robot.audioplayer.SimpleAudio import SimpleAudio
from ai_talking_robot.audioplayer.AudioSpec import *

def generar_onda_seno_int16(frecuencia=440, duracion=1.0, sample_rate=44100, amplitud=0.5):
    t = np.linspace(0, duracion, int(sample_rate * duracion), endpoint=False)
    onda = amplitud * np.sin(2 * np.pi * frecuencia * t)
    return np.int16(onda * 32767)

def generar_onda_seno_float32(frecuencia=440, duracion=1.0, sample_rate=44100, amplitud=0.5):
    t = np.linspace(0, duracion, int(sample_rate * duracion), endpoint=False)
    onda = amplitud * np.sin(2 * np.pi * frecuencia * t)
    return onda.astype(np.float32)

def guardar_wav_desde_array_int16(nombre_archivo, array, sample_rate=44100):
    with wave.open(nombre_archivo, 'wb') as f:
        f.setnchannels(1)
        f.setsampwidth(2)
        f.setframerate(sample_rate)
        f.writeframes(array.tobytes())

def generar_wav_bytes_desde_array_int16(array, sample_rate=44100):
    import io
    buffer = io.BytesIO()
    with wave.open(buffer, 'wb') as f:
        f.setnchannels(1)
        f.setsampwidth(2)
        f.setframerate(sample_rate)
        f.writeframes(array.tobytes())
    return buffer.getvalue()

def test_constructor_con_archivo_wav():
    print("Prueba: Constructor con archivo WAV")
    arreglo = generar_onda_seno_int16()
    ruta_wav = "test_manual.wav"
    guardar_wav_desde_array_int16(ruta_wav, arreglo)
    try:
        factory = SimpleAudioFactory()
        player = factory.create(WavFileSpec(path= ruta_wav))
        player.playAudio()
        print("Reproducción de archivo WAV exitosa.\n")
    except Exception as a:
        print("Error capturado:", a)
        import traceback
        traceback.print_exc()
    finally:
        if os.path.exists(ruta_wav):
            os.remove(ruta_wav)

def test_constructor_con_archivo_mp3():
    print("Prueba: Constructor con archivo MP3")
    # Para esta prueba necesitas tener un archivo mp3 válido.
    # Puedes convertir el wav generado a mp3 usando pydub si tienes ffmpeg instalado.
    try:
        from pydub import AudioSegment
        arreglo = generar_onda_seno_int16()
        ruta_wav = "test_manual.wav"
        ruta_mp3 = "test_manual.mp3"
        guardar_wav_desde_array_int16(ruta_wav, arreglo)
        audio = AudioSegment.from_wav(ruta_wav)
        audio.export(ruta_mp3, format="mp3")
        factory = SimpleAudioFactory()
        player = factory.create(Mp3FileSpec(path=ruta_mp3))
        player.playAudio()
        print("Reproducción de archivo MP3 exitosa.\n")
    except Exception as e:
        print("Error al probar archivo MP3:", e)
    finally:
        for f in ["test_manual.wav", "test_manual.mp3"]:
            if os.path.exists(f):
                os.remove(f)

def test_constructor_con_arreglo_int16():
    print("Prueba: Constructor con arreglo numpy int 16")
    arreglo = generar_onda_seno_int16()
    player = SimpleAudioFactory().create(NumpyArraySpec(data = arreglo, sample_rate=44100))
    player.playAudio()
    print("Reproducción desde arreglo numpy int16 exitosa.\n")

def test_constructor_con_arreglo_float32():
    print("Prueba: Constructor con arreglo numpy float 32")
    arreglo = generar_onda_seno_float32()
    player = SimpleAudioFactory().create(NumpyArraySpec(data = arreglo, sample_rate=44100))
    player.playAudio()
    print("Reproducción desde arreglo numpy float32 exitosa.\n")    

def test_constructor_con_bytes():
    print("Prueba: Constructor con bytes de WAV")
    arreglo = generar_onda_seno_int16()
    wav_bytes = generar_wav_bytes_desde_array_int16(arreglo)
    player = SimpleAudioFactory().create(WavBytesSpec(data = wav_bytes))
    player.playAudio()
    print("Reproducción desde bytes exitosa.\n")

if __name__ == "__main__":
    print("=== Pruebas manuales de DefaultAudioPlayer ===")
    print("Asegúrate de tener altavoces conectados y ffmpeg instalado para la prueba de mp3.")
    test_constructor_con_archivo_wav()
    test_constructor_con_archivo_mp3()
    test_constructor_con_arreglo_int16()
    test_constructor_con_arreglo_float32()
    test_constructor_con_bytes()
    print("=== Pruebas finalizadas ===")
