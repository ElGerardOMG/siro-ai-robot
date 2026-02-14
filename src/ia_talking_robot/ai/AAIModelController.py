import string

class AAIModelController:
    
    ROLE_USER = "user"
    ROLE_MODEL = "model"
    
    def __init__(self):
        pass

    def setInstructions(self, instructions : str | None):
        pass
    
    def addInitialMessage(self, role : str, message : str):
        pass
    
    def clearContext(self):
        pass

    def newConversation(self):     
        pass
        
    def sendMessage(self, message: str) -> str:
        pass

    def getMessage(self, indx: int) -> str:
        pass