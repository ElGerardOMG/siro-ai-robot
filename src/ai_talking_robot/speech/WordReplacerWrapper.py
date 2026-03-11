from ai_talking_robot.speech.AVoiceSynthetizer import AVoiceSynthetizer
from ai_talking_robot.audioplayer import AAudio
from ai_talking_robot.audioplayer.AAudioFactory import AAudioFactory

class WordReplacerWrapepr(AVoiceSynthetizer):

    """
    A simple wrapper that replaces the words provided by the replacing_words dict parameter before
    synthetizing.
    """
    def __init__(self, synthetizer: AVoiceSynthetizer, replacing_words : dict[str,str]):
        self._synthetizer = synthetizer
        self._replacing_words = replacing_words
        

    def synthetize(self, text: str) -> AAudio:
        for word, replacement in self._replacing_words.items():
            text = text.replace(word, replacement)
        return self._synthetizer.synthetize(text)
        

    def getAudio(self) -> AAudio:
        return self._synthetizer.getAudio()
        
