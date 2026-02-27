from ai_talking_robot.audioplayer.AudioFactoryFilter import AudioFactoryFilter
from ai_talking_robot.audioplayer.SimpleAudioFactory import SimpleAudioFactory
from ai_talking_robot.speech.KokoroSynthetizer import KokoroSynthetizer

if __name__ == "__main__":
    print("Iniciando...")
    audioFactory = SimpleAudioFactory()
    audioFilter = AudioFactoryFilter(audioFactory)

    audioFilter.pitch_semitones = -4
    audioFilter.echo_delay = 0.008 
    audioFilter.echo_decay = 0.6
    audioFilter.overlay_delay = 0.01   
    audioFilter.gain = 0.5

    print("Cargando...")
    synthetizer = KokoroSynthetizer(audioFilter, "resources/models/kokoro/kokoro-v1.0.onnx", "resources/models/kokoro/voices-v1.0.bin")
    synthetizer.setConfig(voice="pm_alex", language = "es", speed=1.0)
    print("Reproduciendo")
    result = synthetizer.synthetize("Tu alma ahora es mía")
    result.playAudioAsync()

    while result.isCurrentlyPlaying():
        pass
