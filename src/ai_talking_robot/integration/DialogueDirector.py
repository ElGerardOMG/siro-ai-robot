from ia_talking_robot.sequencer.DefaultMoveSequencer import DefaultMoveSequencer
from ia_talking_robot.speech.KokoroSynthetizer import AVoiceSynthetizer

class DialogueObject:

    def __init__(self, synthetizer : AVoiceSynthetizer, sequencer : DefaultMoveSequencer):
        self.sequencer = sequencer
        self.synthetizer = synthetizer
    

    