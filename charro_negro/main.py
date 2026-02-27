
from ai_talking_robot.speech.KokoroSynthetizer import KokoroSynthetizer
from ai_talking_robot.sequencer.DefaultMoveSequencer import DefaultMoveSequencer
from ai_talking_robot.ai.GoogleAIModel import GoogleAIModel
from ai_talking_robot.audioplayer.SimpleAudioFactory import SimpleAudioFactory
from ai_talking_robot.audioplayer.AudioFactoryFilter import AudioFactoryFilter
from ai_talking_robot.voice.DummyTextRecognition import DummyTextRecognition
from ai_talking_robot.voice.VoskSpeechRecognition import VoskSpeechRecognition
from ai_talking_robot.input.EnterInputActivator import EnterInputActivator
from ai_talking_robot.controllers.MockController import MockController
from ai_talking_robot.controllers.AudioPlayerController import AudioPlayerController
from ai_talking_robot.ai.AAIModelController import AAIModelController
from ai_talking_robot.audioplayer.AudioSpec import WavFileSpec

from ai_talking_robot.sequencer.ComponentEnum import ComponentEnum
from ai_talking_robot.integration.DialogueDirector import DialogueDirector
from ai_talking_robot.integration.Robot import Robot, Status
from ai_talking_robot.integration.CustomFormatter import CustomFormatter

from .SequenceNameDefinition import SequenceNameDefinition
from .ComponentNameDefinition import *


import json
import random
import time
import logging
import sys

if __name__ == "__main__":

    ##### LOGGER ######
    log = logging.getLogger()
    # Agregar el Handler de consola
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.DEBUG)
    #console_formatter = logging.Formatter('[%(module)s]: %(message)s')
    console_handler.setFormatter(CustomFormatter())
    log.addHandler(console_handler)

    # Agregar handler para escribir en archivo también
    file_handler = logging.FileHandler('charro_negro/charro_negro.log', mode='a', encoding='utf-8')
    file_handler.setLevel(logging.INFO)
    file_formatter = logging.Formatter('[%(asctime)s][%(levelname)s][%(module)s]: %(message)s')
    file_handler.setFormatter(file_formatter)
    log.addHandler(file_handler)

    # Cofiguración de los loggers individuales
    logging.getLogger("ai_talking_robot.controllers.MockController").setLevel(logging.WARN)
    logging.getLogger("ai_talking_robot.integration.DialogueDirector").setLevel(logging.DEBUG)
    logging.getLogger("ai_talking_robot.sequencer.DefaultMoveSequencer").setLevel(logging.WARN)
    logging.getLogger("ai_talking_robot.integration.Robot").setLevel(logging.DEBUG)
    log = logging.getLogger(__name__)
    log.setLevel(logging.DEBUG)

    ###### ARCHIVO DE CONFIG ######
    log.info("Leeyendo configuraciones de archivos...")
    with open('charro_negro/config.json', 'r', encoding='utf-8') as f:
        config = json.load(f)

    # Cargar las credenciales desde el archivo
    secrets = None
    with open('charro_negro/secrets.json', 'r') as f:
        secrets = json.load(f)
        
    ###### IA ######
    # Crear un objeto controlador de IA
    log.info("Configurando IA...")
    _ai_model_name = config['ai'].get('model')
    ai = GoogleAIModel(apiKey=secrets["google_api_key"], model=_ai_model_name)

    # Obtener la configuración de la IA
    _ai_instructions = config['ai']['instructions']
    _ai_firstMessage = config['ai']['first_model_message']

    # Agregar la lista de movimientos disponibles a instructions
    # Tomar las que serán excluídas
    _excluded_sequences = config.get('excluded_sequences_from_ai_prompt',[])
    # Agregarlas 1 por 1
    for name, dict in SequenceNameDefinition.items():
        if dict.get("description") is not None:
            if name not in _excluded_sequences:
                _ai_instructions += f"[{name}]: {dict['description']}\n"

    log.debug(f"Instrucciones de IA: {_ai_instructions}")
    log.debug(f"Primer mensaje de IA: {_ai_firstMessage}")
    # Establecer las instrucciones como primer mensaje y el primer mensaje del IA
    ai.addMessage(_ai_instructions, _ai_firstMessage)


    
    #### Reconocimiento de voz ####
    log.info("Inicializando reconocimiento de voz")
    #recognition = DummyTextRecognition()
    recognition = VoskSpeechRecognition(model = config.get('vosk_model_path','resources/models/vosk-model-es-0.42'))

    #### Fábrica de audio ####
    log.info("Inicializando creador de audios")
    audioFactory = SimpleAudioFactory()
    audioFilter = AudioFactoryFilter(audioFactory)
    # Obtener la configuración del filtro del audio
    _audio_filter_config = config.get('audio_filter', {})
    audioFilter.pitch_semitones = _audio_filter_config.get('pitch_semitones', -4)
    audioFilter.echo_delay = _audio_filter_config.get('echo_delay', 0.008)
    audioFilter.echo_decay = _audio_filter_config.get('echo_decay', 0.6)
    audioFilter.overlay_delay = _audio_filter_config.get('overlay_delay', 0.01)
    audioFilter.gain = _audio_filter_config.get('gain', 1.0)


    ### Synthetizador ###
    log.info("Inicializando sintetizador de voz")
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
    log.info("Configurando componentes y controladores")
    input = EnterInputActivator()

    servoController = MockController(Servos,"Servos")
    ledController = MockController(Leds,"Leds")

    
    _audio_config = config.get('sequence_audios', [])

    log.debug(f"Audios leídos: {_audio_config}")
    controllerAudios = [
        audioFactory.create(WavFileSpec(path=p))
        for p in _audio_config
    ]

    audioController = AudioPlayerController(Audios, controllerAudios);

    log.info(f"Inicializando sequencer...")
    sequencer = DefaultMoveSequencer()


    ### Integración e inicialización ###
    log.info(f"Inicializando sistema de diálogo...")
    director = DialogueDirector(synth, sequencer, SequenceNameDefinition)
    log.info(f"Fabricando robot...")
    main = Robot(
        aiModel=ai,
        recognition=recognition,
        sequencer=sequencer,
        inputA=input,
        director=director,
        animations=SequenceNameDefinition
    )


    ### Configuración adicional ###
    log.info(f"Configurando robot...")
    # Nombre del robot
    main.robotName = config.get('robot_name', 'Charro Negro')
    
    # Poner el mensaje inicial como el mensaje inicial de la ia
    main.initial_dialogue_text = _ai_firstMessage

    # Setear las banderas de finalización de la conversación
    main.end_dialogue_flags = config.get('finalization_flags')

    main.idle_animation_name = config.get("idle_sequence")
    # Reemplazo de palabras para correcta pronunciación.
    #main.setReplacingWords(config.get('speech_replacements', []))
    # Determinar cuál es la animación que se reproduce al iniciar
    #main.setStartingSequenceName(config.get('starting_sequence_name','ADEMAN_1'))

    # Crear el bucle "Idle" que reproduce el audio pequeño para evitar que la bocina se apague
    _idle_cfg = config.get('idle', {})
    _audio_wavs = _idle_cfg.get('sound_wavs', ["charro_negro/audios/auxiliar_sound.wav"])
    _audios = [audioFactory.create(WavFileSpec(path=p)) for p in _audio_wavs]
    _play_audio_interval = _idle_cfg.get('play_audio_interval', 5.0)
    
    def sound_loop():
        while True:
            if main.status in [Status.LISTENING, Status.THINKING, Status.WAITING]:
                totalAudios = len(_audios)
                if totalAudios > 0:
                    randomNumber = random.randint(0, totalAudios - 1)
                    _audios[randomNumber].playAudio()
                time.sleep(_play_audio_interval)

    main.idle_behaviour = sound_loop

    log.info(f"Comenzando... ¡{main.robotName} está vivo!")
    ### Comenzar ###
    main.start()
