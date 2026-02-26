
from src.ia_talking_robot.log.ConsoleLogger import ConsoleLogger
from src.ia_talking_robot.speech.KokoroSynthetizer import KokoroSynthetizer
from src.ia_talking_robot.sequencer.DefaultMoveSequencer import DefaultMoveSequencer
from src.ia_talking_robot.ai.GoogleAIModel import GoogleAIModel
from src.ia_talking_robot.audioplayer.SimpleAudioFactory import SimpleAudioFactory
from src.ia_talking_robot.audioplayer.AudioFactoryFilter import AudioFactoryFilter
from src.ia_talking_robot.voice.DummyTextRecognition import DummyTextRecognition
from src.ia_talking_robot.voice.VoskSpeechRecognition import VoskSpeechRecognition
from src.ia_talking_robot.speech.FakeYouVoiceSynthetizer import FakeYouVoiceSynthetizer
from src.ia_talking_robot.input.EnterInputActivator import EnterInputActivator
from src.ia_talking_robot.controllers.MockController import MockController
from src.ia_talking_robot.controllers.AudioPlayerController import AudioPlayerController
from src.ia_talking_robot.ai.AAIModelController import AAIModelController
from src.ia_talking_robot.audioplayer.AudioSpec import WavFileSpec

from .SequenceNameDefinition import SequenceNameDefinition
from .ComponentNameDefinition import *
from .Algorithm import MainAlgorithm
from .Algorithm import Status

import json
import random
import time

if __name__ == "__main__":

    # Cargar la configuración desde el archivo
    with open('darth_vader/config.json', 'r', encoding='utf-8') as f:
        config = json.load(f)

    # Cargar las credenciales desde el archivo
    secrets = None
    with open('darth_vader/secrets.json', 'r') as f:
        secrets = json.load(f)
        
    ###### IA ######
    # Crear un objeto controlador de IA
    _ai_model_name = config['ai'].get('model', 'gemini-2.0-flash-lite')
    ai = GoogleAIModel(apiKey=secrets["google_api_key"], model=_ai_model_name)

    # Obtener la configuración de la IA
    _ai_instructions = config['ai']['instructions']
    _ai_firstMessage = config['ai']['first_model_message']

    # Agregar la lista de movimientos disponibles a instructions
    _excluded_sequences = config.get('excluded_sequences_from_ai_prompt',[])
    for name, dict in SequenceNameDefinition.items():
        if dict.get("description") is not None:
            if name not in _excluded_sequences:
                _ai_instructions += f"[{name}]: {dict['description']}\n"

    #print(_ai_instructions)
    # Establecer las instrucciones
    ai.setInstructions(_ai_instructions)

    # Agregar el primer mensaje como dicho por parte de la IA
    ai.addMessage(AAIModelController.ROLE_MODEL, _ai_firstMessage)
    
    #### Reconocimiento de voz ####
    #recognition = DummyTextRecognition()
    recognition = VoskSpeechRecognition(model = config.get('vosk_model_path','resources/models/vosk-model-es-0.42'))

    #### Fábrica de audio ####
    audioFactory = SimpleAudioFactory()
    audioFilter = AudioFactoryFilter(audioFactory)
    # Obtener la configuración del filtro del audio
    _audio_filter_config = config.get('audio_filter', {})
    audioFilter.pitch_semitones = _audio_filter_config.get('pitch_semitones', -4)
    audioFilter.echo_delay = _audio_filter_config.get('echo_delay', 0.008)
    audioFilter.echo_decay = _audio_filter_config.get('echo_decay', 0.6)
    audioFilter.overlay_delay = _audio_filter_config.get('overlay_delay', 0.01)
    audioFilter.gain = _audio_filter_config.get('gain', 1.0)

    """
    synth = FakeYouVoiceSynthetizer(audioFactory=audioFilter)
    synth.setCookie(secrets["fake_you_cookie"])
    synth.setModel("weight_eayyttcf6rt2v4ty3vd6z8hd6")
    """

    ### Synthetizador ###
    _voice_config = config.get('voice', {})

    synth = KokoroSynthetizer(
        audioFilter,
        onnxFilePath=_voice_config.get('onnx_file_path','resources/models/kokoro/kokoro-v1.0.onnx'),
        voicesBinPath=_voice_config.get('voices_file_path','resources/models/kokoro/voices-v1.0.bin')
    )
    
    synth.setConfig(
        voice=_voice_config.get('voice', 'pm_alex'),
        language=_voice_config.get('language', 'es'),
        speed=_voice_config.get('speed', 1.0)
    )
    

    ### Configuración de los servos ###
    input = EnterInputActivator()

    servoController = MockController(16,"Servo")
    ledController = MockController(4,"Led")

    _audio_config = config.get('sequence_audios', [])

    controllerAudios = [
        audioFactory.create(WavFileSpec(path=p))
        for p in _audio_config
    ]

    audioController = AudioPlayerController(controllerAudios);

    sequencer = DefaultMoveSequencer(
            [
                (servoController, ServoChannelNames),
                (ledController, LedChannelNames),
                (audioController, AudioNames)
            ]    
    )


    
    ### Integración e inicialización ###
    main = MainAlgorithm(
        audioFactory=audioFactory,
        aiModel=ai,
        synthesis=synth,
        recognition=recognition,
        sequencer=sequencer,
        inputA=input
    )

    ### Loggeador ###
    logger = ConsoleLogger(False)
    main.addNewLogger(logger)

    ### Configuración adicional ###

    # Nombre del robot
    main.setRobotName(config.get('robot_name', 'Darth Vader'))
    # Reemplazo de palabras para correcta pronunciación.
    main.setReplacingWords(config.get('speech_replacements', []))
    # Determinar cuál es la animación que se reproduce al iniciar
    main.setStartingSequenceName(config.get('starting_sequence_name','ADEMAN_1'))

    # Crear el bucle "Idle" que reproduce el audio de respiración cuando no habla
    _idle_cfg = config.get('idle', {})
    _breathing_wav = _idle_cfg.get('breathing_wavs', ["darth_vader/audios/breathing.wav"])
    _audios = [audioFactory.create(WavFileSpec(path=p)) for p in _breathing_wav]
    _play_audio_interval = _idle_cfg.get('play_audio_interval', 5.0)

    def breathing_loop():
        while True:
            if main.getStatus() in [Status.LISTENING, Status.THINKING, Status.WAITING]:
                totalAudios = len(_audios)
                if totalAudios > 0:
                    randomNumber = random.randint(0, totalAudios - 1)
                    _audios[randomNumber].playAudio()
                time.sleep(_play_audio_interval)


    main.setIdleLoopBehaviour(breathing_loop)

    ### Comenzar ###
    main.start()
