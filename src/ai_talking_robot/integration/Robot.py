from typing import Any
from ai_talking_robot.audioplayer.AAudioFactory import AAudioFactory
from ai_talking_robot.audioplayer.AAudio import AAudio
from ai_talking_robot.ai.AAIModelController import AAIModelController
from ai_talking_robot.integration.DialogueDirector import DialogueDirector
from ai_talking_robot.voice.ASpeechRecognition import ASpeechRecognition
from ai_talking_robot.speech.AVoiceSynthetizer import AVoiceSynthetizer
from ai_talking_robot.sequencer.DefaultMoveSequencer import DefaultMoveSequencer
from ai_talking_robot.input.AInputActivator import AInputActivator

import logging
import time
import re
import threading
import random

from enum import Enum

log = logging.getLogger(__name__)
print(__name__)

class Status(Enum):
    WAITING = 0
    LISTENING = 1
    THINKING = 2
    SPEAKING = 3

class Robot():

    def __init__(
        self, 
        aiModel : AAIModelController,
        recognition : ASpeechRecognition,
        sequencer : DefaultMoveSequencer,
        inputA : AInputActivator,
        director : DialogueDirector,
        animations : dict[str, str]
        ):

       
        self._aiModel = aiModel
        self._recognition = recognition
        self._sequencer = sequencer
        self._inputA = inputA
        self._director = director
        self._animations = animations

        self.robotName = "Robot"
        self.maxAIAttempts = 5

        self.status = Status.WAITING

        self.end_dialogue_flags : list[str] = None
        
        self.initial_dialogue_text : str = None
        self.idle_animation_name : str = None

        self.idle_behaviour : function = None

        self._initial_dialogue_object = None
        self._idle_animation = None
        
    def start(self):

        self._initialize()

        while True:
          
            self._sequencer.executeSequence(self._idle_animation)

            self._await_initialization()
            
            # Bucle conversacional

            while True:
                recognized = self._listen_user()

                try:
                    response = self._process_ai_response(recognized)
                except:
                    continue
                
                dialogue_object = self._director.parseTextToDialogue(response)

                log.info(f"{self.robotName}> {dialogue_object.getCleanText()}")

                self.status = Status.SPEAKING

                self._director.playDialogue(dialogue_object)

                if self.end_dialogue_flags is not None and any(flag in response for flag in self.end_dialogue_flags):
                    log.info(f"Terminando conversación...")
                    break
            # --- Bucle Conversacional

        # --- Bucle Principal

    """
        def _replaceWords(self, texto : str):
            nuevoTexto = texto
            for t in self._replacingWords:
                nuevoTexto = nuevoTexto.replace(t[0],t[1])

            return nuevoTexto

    """

    def _initialize(self):
        self._initial_dialogue_object = self._director.parseTextToDialogue(self.initial_dialogue_text)
        self._director.synthesize(self._initial_dialogue_object)

        idle_anim_dict = self._animations.get(self.idle_animation_name)

        if idle_anim_dict is not None:
            self._idle_animation = idle_anim_dict.get("sequence")
        else:
            self._idle_animation = []

        if self.idle_behaviour is not None:
            thr = threading.Thread(target = self.idle_behaviour, daemon=True)
            thr.start()

    def _await_initialization(self):
        self.status = Status.WAITING
        log.info("Esperando inicialización...")
        self._inputA.waitForInput()
        self.status = Status.SPEAKING
        log.info("Iniciando ...")
        log.info(f"{self.robotName}> {self._initial_dialogue_object.getCleanText()}")
        self._director.playDialogue(self._initial_dialogue_object)

        self._aiModel.newConversation()

    def _listen_user(self) -> str:
        self.status = Status.LISTENING
        while True:
            recognized = None
            try:
                log.info("Comenzando reconocimiento de voz")
                recognized = self._recognition.startRecognition()
                if recognized is None or recognized == "":
                    recognized = "(*silencio)"
                log.info(f"Usuario> {recognized}")
                return recognized
            except Exception as e:
                log.exception("Fallo en el reconocimiento ")
                

    def _process_ai_response(self, recognized: str) -> str:
        self.status = Status.THINKING
        attempts = 0

        while True:
            try:
                log.info(f"Enviando mensaje a IA")
                response = self._aiModel.sendMessage(recognized)
                log.debug(f"Respuesta obtenida: {response}")
                return response
            except Exception as E:
                if attempts >= self.maxAIAttempts:
                    log.exception("Fallo total en el procesamiento de IA ")
                    raise
                else:
                    log.error(f"Fallo en el procesamiento de IA: {E}")
                    attempts += 1
                    continue

    
