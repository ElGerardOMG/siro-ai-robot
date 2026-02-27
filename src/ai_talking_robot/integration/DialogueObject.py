from enum import Enum
from io import StringIO
from typing_extensions import Any

from ai_talking_robot.audioplayer.AAudio import AAudio

class _dialogueObject:
    def __init__(self, 
        animation_name : str = None, 
        dialogue_text : str = None, 
        audio : AAudio = None):

        self.animation = animation_name
        self.dialogue_text = dialogue_text
        self.audio : AAudio = audio
        
        if (dialogue_text.isspace()) or (len(dialogue_text) == 0) or (dialogue_text is None):
            self.audio_status = DialogueStates.READY
        else:
            self.audio_status = DialogueStates.EMPTY if audio is None else DialogueStates.READY

class DialogueObject:
    def __init__(self):
        self._items : list[_dialogueObject] = []
    
    def insertNew(self, 
        animation_name : str = None, 
        dialogue_text : str = None, 
        audio : AAudio = None):

        self._items.append(_dialogueObject(
            animation_name = animation_name, 
            dialogue_text=dialogue_text, 
            audio = audio)
        )

    def items(self):
        return self._items

    def getCleanText(self) -> str:
        string = StringIO()
        for item in self._items:
             string.write(f'{item.dialogue_text.strip()} ')
        res = string.getvalue()
        string.close()
        return res

class DialogueStates(Enum):
    EMPTY = 0
    CREATING = 1
    READY = 2
    PLAYING = 3
    FAILED = 4