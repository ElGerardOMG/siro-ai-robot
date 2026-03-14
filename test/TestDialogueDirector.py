from ai_talking_robot.audioplayer import SimpleAudioFactory
from ai_talking_robot.sequencer.DefaultMoveSequencer import DefaultMoveSequencer
from ai_talking_robot.integration.DialogueDirector import DialogueDirector
from ai_talking_robot.speech.KokoroSynthetizer import KokoroSynthetizer
from ai_talking_robot.controllers.MockController import MockController

from .SampleTestAnimationSuite import *

import logging
import sys

log = logging.getLogger()

from test.SampleTestAnimationSuite import *
if __name__ == "__main__":

    #logging.basicConfig(filename='myapp.log', level=logging.INFO)
    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(logging.DEBUG)
    formatter = logging.Formatter('[%(module)s]: %(message)s')
    handler.setFormatter(formatter)
    log.addHandler(handler)
    log.setLevel(logging.DEBUG)
    
    log.debug("Initialized...")

    sample_text = ["[ANIMACION_1] El Conejo que saltaba por el campo.\n"
     "[ANIMACION_2] era feliz porque saltaba.\n"
     "[ANIMACION_3] Su única ambición era saltar y saltar, libre como el viento [FIN]"]

    controller = MockController(SampleComponents, name = "Controlador")

    audio_factory = SimpleAudioFactory()
    sequencer = DefaultMoveSequencer()
    sequencer.valueUpdateInterval = 1.0

    synth = KokoroSynthetizer(audio_factory, "resources/models/kokoro/kokoro-v1.0.onnx", "resources/models/kokoro/voices-v1.0.bin")
    synth.setConfig(voice="pm_alex", language = "es", speed=1.0)
    synth.synthetize("Esto es una prueba xd").playAudio()

    director = DialogueDirector(synth, sequencer, SampleTestSequences)
    log.debug("Parsing...")
    
    obj = director.parseTextToDialogue(sample_text[0])
    
    log.debug("Playing...")
    director.playDialogue(obj)