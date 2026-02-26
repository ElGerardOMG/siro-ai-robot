#TODO: Este archivo es fuertemente dependiente de "SequenceNameDefinition"
# sería conveniente desacoplarlo, aunque por ahora es funcional así.

from src.ia_talking_robot.audioplayer.AAudioFactory import AAudioFactory
from src.ia_talking_robot.audioplayer.AAudio import AAudio
from src.ia_talking_robot.ai.AAIModelController import AAIModelController
from src.ia_talking_robot.voice.ASpeechRecognition import ASpeechRecognition
from src.ia_talking_robot.speech.AVoiceSynthetizer import AVoiceSynthetizer
from src.ia_talking_robot.sequencer.DefaultMoveSequencer import DefaultMoveSequencer
from src.ia_talking_robot.input.AInputActivator import AInputActivator
from src.ia_talking_robot.log.CLoggableObject import CLoggableObject
from src.ia_talking_robot.log.LogLevel import LogLevel


from .SequenceNameDefinition import SequenceNameDefinition

import time
import re
import threading
import random

from enum import Enum

class Status(Enum):
    WAITING = 0
    LISTENING = 1
    THINKING = 2
    SPEAKING = 3

class MainAlgorithm(CLoggableObject):

    def __init__(
        self, 
        audioFactory : AAudioFactory,
        aiModel : AAIModelController,
        synthesis : AVoiceSynthetizer,
        recognition : ASpeechRecognition,
        sequencer : DefaultMoveSequencer,
        inputA : AInputActivator
         ):

        CLoggableObject.__init__(self)
        self.audioFactory = audioFactory
        self.aiModel = aiModel
        self.synthesis = synthesis
        self.recognition = recognition
        self.sequencer = sequencer
        self.inputA = inputA

        self._robotName = "Robot"
        self._maxAIAttempts = 5
        #self._backAudioPlayInterval = 5
        #self._backAudioPlaysAtStatuses : list[Status] = []
        #self._backAudios : list[AAudio] = []
        self._idleBehaviour : function = lambda : None
        self._replacingWords : list[tuple[str, str]] = []
        
        self._startingDialogueAudio : AAudio = None
        self._startingSequence : str = ""

        self._status = Status.WAITING
    

        
    def start(self):

        self._presynthetize_start_dialogue()
        self._initialize_idle()
        
        while True:
            finishing = False

            self._await_initialization()

            # Bucle conversacional
            while True:
                recognized = self._listen_user()

                response = self._process_ai_response(recognized)

                secuence_dialogue_pairs, clean_message, finishing = self._parse_response(response)
                self.logMessage(f"[{self._robotName}]: {clean_message}",LogLevel.MESSAGE)

                synthetized_audios : list[AAudio] = [None for _ in range(len(secuence_dialogue_pairs))]
                ready_audios : list[bool] = [False for _ in range(len(secuence_dialogue_pairs))]

                self._status = Status.SPEAKING
                hilo = threading.Thread(target=self._batch_synthesis, args=(secuence_dialogue_pairs, synthetized_audios, ready_audios), daemon=True)
                hilo.start()

                previousAudio = self._speak_and_move(secuence_dialogue_pairs, synthetized_audios, ready_audios)

                while previousAudio is not None and previousAudio.isCurrentlyPlaying():
                    pass

                if finishing:
                    self.logMessage(f"Terminando conversación...", LogLevel.INFO)
                    break
            # --- Bucle Conversacional

        # --- Bucle Principal

    # --- Setters y Getters importantes --- #
    def setRobotName(self, name : str):
        self._robotName = name    

    def setReplacingWords(self, wordList : list[tuple[str, str]]):
        self._replacingWords = wordList
        
    def setIdleLoopBehaviour(self, func):
        self._idleBehaviour = func

    def setStartingSequenceName(self, startingSequence : str):
        self._startingSequence = startingSequence

    def getStatus(self):
        return self._status


    # --- Métodos privados extraídos --- #

    def _replaceWords(self, texto : str):
        nuevoTexto = texto
        for t in self._replacingWords:
            nuevoTexto = nuevoTexto.replace(t[0],t[1])

        return nuevoTexto


    def _presynthetize_start_dialogue(self):
        initialDialogueRaw = self._replaceWords(self.aiModel.getMessage(0))
        _, initialDialogueClean, _ = self._parse_response(initialDialogueRaw)
        self._startingDialogueAudio = self.synthesis.synthetize(initialDialogueClean)

    def _initialize_idle(self):
        self.sequencer.executeSequence(SequenceNameDefinition["IDLE"]["sequence"])
        thr = threading.Thread(target=self._idleBehaviour, daemon=True)
        thr.start()

    def _await_initialization(self):
        self._status = Status.WAITING
        self.logMessage("Esperando inicialización...", LogLevel.INFO)
        self.inputA.waitForInput()

        self._status = Status.SPEAKING
        self.logMessage("Iniciando..", LogLevel.MESSAGE)
        self.logMessage(f"[{self._robotName}]: {self.aiModel.getMessage(0)}", LogLevel.MESSAGE)
        
        self.sequencer.executeSequenceAsync(SequenceNameDefinition[self._startingSequence]["sequence"]);
        self._startingDialogueAudio.playAudio()

        self.aiModel.newConversation()

    def _listen_user(self) -> str:
        self._status = Status.LISTENING
        while True:
            recognized = None
            try:
                self.logMessage(f"Comenzando reconocimiento de voz", LogLevel.INFO)
                recognized = self.recognition.startRecognition()
                if recognized is None or recognized == "":
                    recognized = "(*silencio)"
                self.logMessage(f"[Usuario]: {recognized}", LogLevel.MESSAGE)
                return recognized
            except Exception as e:
                self.logMessage(f"Fallo en el reconocimiento: {e.with_traceback}", LogLevel.ERROR)

    def _process_ai_response(self, recognized: str) -> str:
        self._status = Status.THINKING
        attempts = 0
        while True:
            try:
                self.logMessage(f"Enviando mensaje a la IA", LogLevel.INFO)
                response = self.aiModel.sendMessage(recognized)
                self.logMessage(f"Respuesta obtenida: {response}", LogLevel.INFO)
                return response
            except Exception as E:
                if attempts >= self._maxAIAttempts:
                    self.logMessage(f"Fallo total en el procesamiento de IA: {E.with_traceback}", LogLevel.ERROR)
                    raise
                else:
                    self.logMessage(f"Fallo en el procesamiento de IA: {E}", LogLevel.ERROR)
                    attempts += 1
                    continue

    def _parse_response(self, response: str):
        splitted = re.split(r'(\[[^\]]+\])', response)[1:]
        secuence_dialogue_pairs = []
        clean_message = ""
        pair = [None, None]
        indx = 0
        finishing = False
        for element in splitted:
            if element.find("[") >= 0:
                if pair[0] is not None:
                    secuence_dialogue_pairs.append(pair)
                    indx += 1
                    pair = [None, None]
                element = element[1:-1]
                if element == "FIN":
                    finishing = True
                else:
                    pair[0] = element
            else:
                if pair[1] is not None:
                    secuence_dialogue_pairs.append(pair)
                    indx += 1
                    pair = [None, None]
                element = element.replace("\n", "")
                pair[1] = element
                clean_message += element
        secuence_dialogue_pairs.append(pair)
        return secuence_dialogue_pairs, clean_message, finishing

    def _batch_synthesis(self, secuence_dialogue_pairs: list[list], synthetized_audios: list, ready_audios: list):
        try:
            audio_index = 0
            for secuence_name, dialogue in secuence_dialogue_pairs:
                if dialogue is None or dialogue.isspace() or dialogue == "":
                    synthetized_audios[audio_index] = None
                    ready_audios[audio_index] = True
                    audio_index += 1
                    continue
                self.logMessage(f"Sintetizando: {dialogue}", LogLevel.INFO)
                dialogue = self._replaceWords(dialogue)
                synthetized_audios[audio_index] = self.synthesis.synthetize(dialogue)
                ready_audios[audio_index] = True
                audio_index += 1
                self.logMessage(f"Síntesis correcta", LogLevel.INFO)
        except Exception as E:
            self.logMessage(f"Fallo al sintetizar audio: {E}", LogLevel.ERROR)
            raise E

    def _speak_and_move(self, secuence_dialogue_pairs: list[list], synthetized_audios: list, ready_audios: list):
        indx = 0
        previousAudio : AAudio = None
        self.idle = False
        for sequence_name, dialogue in secuence_dialogue_pairs:
            while not ready_audios[indx]:
                pass
            if previousAudio is not None:
                while previousAudio.isCurrentlyPlaying():
                    pass
            if synthetized_audios[indx] is not None:
                synthetized_audios[indx].playAudioAsync()
                previousAudio = synthetized_audios[indx]
            if sequence_name is not None:
                sequence = SequenceNameDefinition[sequence_name]["sequence"]
                if self.sequencer.isExecutingSequence():
                    self.logMessage(f"Cancelando secuencia anterior...", LogLevel.INFO)
                    self.sequencer.cancelCurrentSequence()
                if synthetized_audios[indx] is None:
                    self.logMessage(f"Ejecutando secuencia síncrona {sequence_name}..", LogLevel.INFO)
                    self.sequencer.executeSequence(sequence)
                else:
                    self.logMessage(f"Ejecutando secuencia asíncrona {sequence_name}..", LogLevel.INFO)
                    self.sequencer.executeSequenceAsync(sequence)
                    
            indx += 1
            pass
        return previousAudio

