from concurrent.futures import ThreadPoolExecutor
import re
import threading
import logging
import time

from ai_talking_robot.audioplayer.AAudio import AAudio
from ai_talking_robot.integration.DialogueObject import DialogueObject
from ai_talking_robot.integration.DialogueObject import DialogueStates
from ai_talking_robot.sequencer.DefaultMoveSequencer import DefaultMoveSequencer
from ai_talking_robot.speech.KokoroSynthetizer import AVoiceSynthetizer

log = logging.getLogger(__name__)
print(__name__)
class DialogueDirector:

    def __init__(self, synthetizer : AVoiceSynthetizer, sequencer : DefaultMoveSequencer, availible_animations : dict[str, dict]):
        self.sequencer = sequencer
        self.synthetizer = synthetizer
        self.animations = availible_animations
        self.fall_back_animation_name :str = None

    # Sintetizar sin reproducir
    def synthesize(self, dialogues : DialogueObject):
        for dialogue in dialogues.items(): 
            try:
                if dialogue.audio_status in [DialogueStates.EMPTY, DialogueStates.FAILED]:
                    log.info("Sintetizado: " + dialogue.dialogue_text)
                    dialogue.audio_status = DialogueStates.CREATING
                    audio = self.synthetizer.synthetize(text = dialogue.dialogue_text)
                    dialogue.audio = audio
                    dialogue.audio_status = DialogueStates.READY
                    log.debug("Síntesis completa")
                else:
                    log.debug("Nada que sintetizar")
                    continue

            except Exception:
                log.exception("Error sintetizado: ")
                dialogue.audio_status = DialogueStates.FAILED
                continue
        log.debug("Síntesis completa de todos los audios")
            
    # Reproducir mientras se van sintetizando
    def playDialogue(self, dialogues : DialogueObject):

        # Iniciar la síntesis de fondo
        log.debug("Iniciando hilo de síntesis...")
        threading.Thread(target=self.synthesize, args=(dialogues,), daemon=True).start()

        previousAudio : AAudio = None

        for dialogue in dialogues.items(): 
            
            # Esperar a que esté ready
            while dialogue.audio_status not in [DialogueStates.READY, DialogueStates.FAILED]:
                #log.debug(f"Esperando a síntesis completa, estado: {dialogue.audio_status}")
                time.sleep(0.1)
                

            # Ver que el audio previo no se esté reproduciendo
            if previousAudio is not None:
                while previousAudio.isCurrentlyPlaying():
                    pass
            
            # Cambiar el estado a "PLAYING"
            log.debug("Reproduciendo...")
            dialogue.audio_status = DialogueStates.PLAYING

            # Reproducir el audio, si existe
            if dialogue.audio is not None:
                log.debug("Reproduciendo Audio")
                dialogue.audio.playAudioAsync()

            # Reproducir la animación, si existe
            if dialogue.animation is not None:
                
                # Obtener la animación
                animation_dict = self.animations.get(dialogue.animation)

                # Obtenerla, si es nula, obtener una default
                if animation_dict is not None:
                    animation = animation_dict.get("sequence")
                    animation_name = dialogue.animation
                else:
                    log.warning(f"Animación {dialogue.animation} no encontrada, usando fallback")

                    if self.fall_back_animation_name is not None:
                        animation_dict = self.animations.get(self.fall_back_animation_name)
                        animation = animation_dict.get("sequence")
                        animation_name = self.fall_back_animation_name
                    else:
                        animation = []
                        animation_name = "Empty"
                    pass
                
                # Cancelar ejecución, si la hay
                self.sequencer.cancelExecution()

                # Si hay audio, reproducir la animación en forma  no bloqueante.
                # Sino, en forma bloqueante
                if dialogue.audio is not None:
                    log.info(f"Reproduciendo animación asíncrona {animation_name}")
                    threading.Thread(target=self.sequencer.executeSequence, args=(animation,), daemon=True).start()
                else:
                    log.info(f"Reproduciendo animación síncrona {animation_name}")
                    self.sequencer.executeSequence(animation)
            
            # Asignar al previous audio, el actual
            previousAudio = dialogue.audio

            # Devolver el estado a ready
            dialogue.audio_status = DialogueStates.READY
        
        # end for

        log.debug(f"Esperando último audio")
        # Esperar a que el audio previo termine, si lo hay
        if previousAudio is not None:
            while previousAudio.isCurrentlyPlaying():
                pass

        
    

    def parseTextToDialogue(self, text : str) -> DialogueObject:
        splitted = re.split(r'(\[[^\]]+\])', text)[1:]

        dialogue_object = DialogueObject()

        current_animation = None
        current_text = None

        for element in splitted:
            if "[" in element:
                if current_animation is not None:

                    dialogue_object.insertNew(animation_name=current_animation, dialogue_text=current_text)

                    current_animation = None
                    current_text = None
                
                current_animation = element[1:-1]
            else:
                if current_text is not None:

                    dialogue_object.insertNew(animation_name=current_animation, dialogue_text=current_text)

                    current_animation = None
                    current_text = None

                current_text = element.replace("\n","")

        dialogue_object.insertNew(animation_name=current_animation, dialogue_text=current_text)
        
        return dialogue_object
