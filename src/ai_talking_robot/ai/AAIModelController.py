import string

class AAIModelController:
       
    def __init__(self):
        pass

    @property
    def systemInstructions(self):
        pass
    
    @systemInstructions.setter
    def systemInstructions(self, instructions: str | None):
        pass

    def newConversation(self):     
        pass

    def addMessage(self, userMessage : str, modelResponse : str):
        pass
    
    def clearHistory(self):
        pass
        
    def sendMessage(self, message: str) -> str:
        pass

    def getMessage(self, indx: int) -> str:
        pass