import json
import string
import requests
import re
import uuid
import time

from .AVoiceSynthetizer import AVoiceSynthetizer

from ..log.CLoggableObject import CLoggableObject
from ..log.LogLevel import LogLevel

from ..audioplayer.AAudioFactory import AAudioFactory

from ..audioplayer.AudioSpec import WavBytesSpec

LOGIN_URL = "https://api.fakeyou.com/v1/login"
INFERENCE_URL = "https://api.fakeyou.com/tts/inference"
JOB_URL = "https://api.fakeyou.com/tts/job"
AUDIO_URL = "https://cdn-2.fakeyou.com"

class FakeYouVoiceSynthetizer(AVoiceSynthetizer, CLoggableObject):

    """
        Sinterizador de FakeYou.com
        Hace peticiones al servidor, por lo que sólo se requiere
        de conexión a internet.
        Basado en la documentación de: https://docs.fakeyou.com/#/

    """
    def __init__(self, audioFactory : AAudioFactory):
        AVoiceSynthetizer.__init__(self,audioFactory)
        CLoggableObject.__init__(self)
        self.model = ""
        self.cookie = ""
        self.jobToken = ""
        self.synthetizing = False
        self.audio = None
        pass


    """
        Performs synthetizeAsync and then getAudio. Returns the synthetized audio
        using the specified text.
        Blocks the current thread
    """
    def synthetize(self, text: str):
        self.synthetizeAsync(text)
        return self.getAudio()
       
    """
        Just sends a synth request to Server with the specified text to synthetize.
        This method doesn't block the current thread
    """
    def synthetizeAsync(self, text: str):
        self.synthetizing = True
        self.audio = None
        uuidToken = str(uuid.uuid4())
        

        data = {
            "uuid_idempotency_token": uuidToken,
            "tts_model_token": self.model,
            "inference_text": text
        }

        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Cookie": self.cookie
        }
      
        try:
            response = requests.post(
                INFERENCE_URL,
                json=data,
                headers=headers,
                timeout=10  
            )

            response.raise_for_status()
            
            if response.status_code == 200:
                response_json = response.json()
                self.jobToken = response_json['inference_job_token']
            else:
                raise RuntimeError(f"Error: {response.status_code}, response: {response.text}")              
        except requests.exceptions.Timeout:
            raise RuntimeError("Request Timeout");
        except requests.exceptions.RequestException as e:
            raise RuntimeError(f"Request Error: {e}");
        except json.JSONDecodeError as e:
            raise RuntimeError(f"Error while parsing response: {e}");
        pass

    
    """
        Constantly sends requests for audio status until server confirms that the audio is fully
        synthetized. Then, it creates an audio object using the provided AAudioFactory and
        then returns it.

        The audio will remain until synshetizeAsync or synthetize are called again, therefore 
        additional calls to this method without synthetizing again will simply return the 
        already obtained audio.

        If synthetizeAsync or synthetize has not been called before, getAudio will return None

        This method blocks the current thread
    """

    def getAudio(self):
        if not self.synthetizing:
            return self.audio

        url = f"{JOB_URL}/{self.jobToken}"
        
        headers = {
            "Accept": "application/json",
        }

        self.logMessage(f"Iniciando monitoreo de la síntesis {self.jobToken}", LogLevel.INFO)
        
        while True:
            try:
                response = requests.get(url, headers=headers, timeout=10)
                response.raise_for_status()
                
                job_data = response.json()
                
                if not job_data.get("success"):
                    raise Exception(f"La API reportó error: {job_data}")
                    
                status = job_data["state"]["status"]
                self.logMessage(f"Estado actual: {status}", LogLevel.INFO)
                
                # Tarea fallida
                if status in ["complete_failure", "dead"]:
                    self.synthetizing = False
                    raise Exception(f"La tarea falló con estado: {status}")

                # Tarea completada
                if status == "complete_success":
                    self.synthetizing = False
                    self.logMessage("¡Síntesis de audio completada exitosamente!", LogLevel.INFO)
                    
                    # Obtener la ruta del archivo de audio
                    audio_path = job_data["state"]["maybe_public_bucket_wav_audio_path"]
                    if audio_path:
                        self.audio = self._downloadAudio(audio_path)
                        return self.audio
                    else:
                        raise Exception("No se encontró la ruta del archivo de audio")
                         
                # Estado intermedio, continuar esperando
                self.logMessage(f"Estado intermedio: {status}, esperando...", LogLevel.INFO)
                time.sleep(0.2) 
                
            except requests.exceptions.Timeout:
                self.logMessage("Timeout en la petición, reintentando...", LogLevel.WARNING)
                time.sleep(1)
            except requests.exceptions.RequestException as e:
                self.logMessage(f"Error de red: {e}, reintentando...", LogLevel.WARNING)
                time.sleep(1)
            except json.JSONDecodeError as e:
                self.logMessage(f"Error parseando JSON: {e}, reintentando...", LogLevel.WARNING)
                time.sleep(1)
            except Exception as e:
                self.synthetizing = False
                self.logMessage(f"Error inesperado: {e}", LogLevel.ERROR)
                raise


    def _downloadAudio(self, audio_path):
        headers = {
            "Accept": "application/json",
        }

        audio_url = f"{AUDIO_URL}{audio_path}"
        self.logMessage(f"Descargando audio de: {audio_url}", LogLevel.MESSAGE)
        
        audio_response = requests.get(audio_url, headers=headers, timeout=3)
        audio_response.raise_for_status()
        
        #return self.audioFactory.createAudioObject(audio_response.content, AudioSource.WAV_BYTES)
        return self.audioFactory.create(WavBytesSpec(audio_response.content))
   
    def setModel(self, modelId: str):
        self.model = modelId

    def authenticate(self, usernameOrEmail:str, password: str):
        data = {
            "username_or_email": usernameOrEmail,
            "password": password
        }
        try:
            response = requests.post(
                LOGIN_URL,
                json=data, 
                headers={"Content-Type": "application/json"}
            )
            response.raise_for_status()
            
            if "set-cookie" in response.headers:
                set_cookie_header = response.headers["set-cookie"]
                match = re.search(r'^\w+\.=([^;]+)', set_cookie_header)
                if match:
                    self.cookie = match.group(1)
            
        except requests.exceptions.RequestException as e:
            self.logMessage(f"Error en la petición: {e}", LogLevel.ERROR)
        except json.JSONDecodeError as e:
            self.logMessage(f"Error parseando respuesta: {e}", LogLevel.ERROR)

    def getCookie(self):
        return self.cookie

    def setCookie(self, cookie: string):
        self.cookie = cookie


