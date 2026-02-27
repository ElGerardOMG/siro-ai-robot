#from google import genai
from google.genai import types, Client
from .AAIModelController import AAIModelController

class GoogleAIModel(AAIModelController):
    
    def __init__(self, apiKey : str, model: str):
        self._client = Client(api_key=apiKey)
        self._model = model
        self._chat : types.Chat = None
        
        self._systemInstructions : types.GenerateContentConfig = None
        self._initialHistory = []   

    #NOTA: No todos los modelos de Google (como los Gemma) permiten system instructions
    # Por eso será simplemente mejor evitar estos
    @property
    def systemInstructions(self):
        if self._systemInstructions is not None:
            return self._systemInstructions.system_instruction
        return None
    
    @systemInstructions.setter
    def systemInstructions(self, instructions: str | None):
        if instructions is None:
            self._systemInstructions = None
        else:
            self._systemInstructions = types.GenerateContentConfig(system_instruction=instructions)

    def addMessage(self, userMessage : str, modelResponse : str):
        if self._chat is None:
            self._initialHistory.extend([
                types.Content(parts=[types.Part(
                text=userMessage
            ),],role='user'),

                types.Content(parts=[types.Part(
                    text=modelResponse
                ),
                ], role='model' ),
            ])
            return
            
        self._chat.record_history(
            user_input=types.Content(parts=[types.Part(
                text=userMessage
            ),
            ],role='user'
            ), model_output= [types.Content(parts=[types.Part(
                text=modelResponse
            ),
            ], role='model' ),], 
            automatic_function_calling_history = None,
            is_valid = True
        )
    
    def clearHistory(self):
        self._initialHistory = []
        self._chat = None

    def newConversation(self):     
        self._chat = self._client.chats.create(
            model = self._model,
            config = self._systemInstructions,
            history = self._initialHistory
        )
        
    def sendMessage(self, message: str) -> str:
        if self._chat is None:
            raise ValueError("Chat has been not initialized!")
        response = self._chat.send_message(message = message)
        return response.text
        


    def getMessage(self, indx: int) -> str:
        if self._chat is None:
            return self._initialHistory[indx].parts[0].text

        return self._chat.get_history()[indx].parts[0].text

        