from google import genai
from google.genai import types
from .AAIModelController import AAIModelController

class GoogleAIModel(AAIModelController):
    
    def __init__(self, apiKey : str, model: str):
        self.client = genai.Client(api_key=apiKey)
        self.model = model
        self.chat = None

        self.instructions = []
        self.initialHistory = []


    def setInstructions(self, instructions : str | None):
        if instructions is None:
            self.instructions = []
            return

        self.instructions = [
            types.Content(role="user", parts=[types.Part(text=instructions)])
        ]
    
    
    def addInitialMessage(self, role : str, message : str):
        self.initialHistory.append(
            types.Content(role=role, parts=[types.Part(text=message)])
        )
    
    def clearMemory(self):
        self.setInstructions(None)
        self.initialHistory = []
        self.chat = None

    def newConversation(self):     
        self.chat = self.client.chats.create(
            model = self.model,
            history = self.instructions + self.initialHistory
        )
        
    def sendMessage(self, message: str) -> str:
        response = self.chat.send_message(message = message)
        return response.text

    # Note: The first message (0) is the first message after the instructions. Therefore
    # instructions are not considered the first message.
    def getMessage(self, indx: int) -> str:
        if self.chat is None:
            return self.initialHistory[indx].parts[0].text

        return self.chat.get_history()[indx + 1].parts[0].text

        