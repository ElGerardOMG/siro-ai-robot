import numpy as np


from ai_talking_robot.audioplayer.SimpleAudioFactory import SimpleAudioFactory
from ai_talking_robot.controllers.AudioPlayerController import AudioPlayerController
from ai_talking_robot.sequencer.DefaultMoveSequencer import DefaultMoveSequencer
from ai_talking_robot.audioplayer.AudioSpec import NumpyArraySpec
from ai_talking_robot.controllers.ParallelControlerWrapper import ParallelControllerWrapper

from ai_talking_robot.controllers.MockController import MockController

from test.SampleTestAnimationSuite import *

import logging
import sys
log = logging.getLogger()


if __name__ == "__main__":

    #logging.basicConfig(filename='myapp.log', level=logging.INFO)
    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(logging.DEBUG)
    formatter = logging.Formatter('[%(module)s]: %(message)s')
    handler.setFormatter(formatter)
    log.addHandler(handler)
    log.setLevel(logging.DEBUG)
    

    servoController = MockController(SampleComponents,"Servo")
    servoController = ParallelControllerWrapper(servoController)

    audioFactory = SimpleAudioFactory()

    audios = []
    for i in range(3):
        duracion = 3.0
        sample_rate = 44100
        frecuencia = 400 + 40 * i
        amplitud = 0.02
        t = np.linspace(0, duracion, int(sample_rate * duracion), endpoint=False)
        onda = amplitud * np.sin(2 * np.pi * frecuencia * t)
        onda = onda.astype(np.float32)
        onda_int16 = np.int16(onda * 32767)

        audios.append(audioFactory.create(NumpyArraySpec(onda_int16, sample_rate)))

    audioController = ParallelControllerWrapper(AudioPlayerController(SampleComponentsAudios, audios))

    sequencer = DefaultMoveSequencer()
    sequencer.valueUpdateInterval = 0.5

    print("Ejecutando con sonido...")

    sequencer.valueUpdateInterval = 0.2

    sequencer.executeSequence(FIN_ANIM)