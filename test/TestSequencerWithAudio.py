from src.ia_talking_robot.audioplayer import AudioSource
from src.ia_talking_robot.audioplayer.SimpleAudioFactory import SimpleAudioFactory
from src.ia_talking_robot.controllers.AudioPlayerController import AudioPlayerController
from src.ia_talking_robot.sequencer.DefaultMoveSequencer import DefaultMoveSequencer
from src.ia_talking_robot.sequencer.SampleComponentDefinition import *
from src.ia_talking_robot.sequencer.SampleAudioSequence import SampleAudioSequence
from src.ia_talking_robot.audioplayer.AudioSpec import WavFileSpec
from src.ia_talking_robot.log.ConsoleLogger import ConsoleLogger

from src.ia_talking_robot.controllers.MockController import MockController
    


if __name__ == "__main__":
    logger = ConsoleLogger()
    servoController = MockController(16,"Servo")
    servoController.addNewLogger(logger)

    audioFactory = SimpleAudioFactory()
    
    audio_1 = audioFactory.create(WavFileSpec(path="src/darth_vader/audios/saber_on.wav"))
    audio_2 = audioFactory.create(WavFileSpec(path="src/darth_vader/audios/saber_off.wav"))
    audio_3 = audioFactory.create(WavFileSpec(path="src/darth_vader/audios/attack.wav"))


    audioController = AudioPlayerController([audio_1, audio_2, audio_3])

    sequencer = DefaultMoveSequencer(
        [
            (servoController, Servos),
            (audioController, Audios),

        ]
    )
    print("Ejecutando con sonido...")
    sequencer.setTimePartionSize(0.2)

    sequencer.executeSequence(SampleAudioSequence)