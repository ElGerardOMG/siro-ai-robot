from src.ia_talking_robot.audioplayer.AudioFactoryFilter import AudioFactoryFilter
from src.ia_talking_robot.audioplayer.SimpleAudioFactory import SimpleAudioFactory
from src.ia_talking_robot.speech.KokoroSynthetizer import KokoroSynthetizer

if __name__ == "__main__":
    print("Iniciando...")
    audioFactory = SimpleAudioFactory()
    audioFilter = AudioFactoryFilter(audioFactory)

    audioFilter.pitch_semitones = -4
    audioFilter.echo_delay = 0.008 
    audioFilter.echo_decay = 0.6
    audioFilter.overlay_delay = 0.1   
    audioFilter.gain = 0.01 
    print("Cargando...")
    synthetizer = KokoroSynthetizer(audioFilter, "src/resources/models/kokoro/kokoro-v1.0.onnx", "src/resources/models/kokoro/voices-v1.0.bin")
    synthetizer.setConfig(voice="pm_alex", language = "es", speed=1.0)
    print("Reproduciendo síncrono...")
    result = synthetizer.synthetize("¡Únete!, aún hay tiempo, No te dejes destruir como lo hizo Ohbi guán")
    result.playAudio()

    print("Reproduciendo asíncrono...")
    synthetizer.synthetizeAsync("No...... Luc...... Llo...... soy...... ¡Tu padre!..., ")
    audio = synthetizer.getAudio()

    

    synthetizer.synthetizeAsync(f"¡Busca en tus sentimientos!... ¡tú sabes que es cierto!")

    audio.playAudio()

    audio2 = synthetizer.getAudio()

    audio2.playAudio()

    synthetizer.synthetize(f"")