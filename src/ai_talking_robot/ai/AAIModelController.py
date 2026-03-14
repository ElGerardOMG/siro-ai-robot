import string

class AAIModelController:
       
    """
        AAIModelController es una clase para usar una IA. Puede ser a través de API o local
        si se implementa correctamente. Esta clase guarda y maneja el historial de mensajes
        que se hacen. Hay dos tipos de historial, el inicial y el actual. Ambos funcionan como
        uno solo historial, excepto que el inicial es persistente y no se borra al iniciar una
        nueva conversación, haciendo que cada mensaje posterior comienzen con ese historial de
        mensajes inicial.
    """
    def __init__(self):
        pass

    @property
    def systemInstructions(self):
        pass
    
    @systemInstructions.setter
    def systemInstructions(self, instructions: str | None):
        pass


    def newConversation(self):
        """
            Crea una nueva conversación activa. La conversación se cargará automáticamente con los
            mensajes del historial inicial.
        """     
        pass

    def addMessage(self, userMessage : str, modelResponse : str):
        """
            Guarda un mensaje nuevo al historial sin enviarlo a la IA. Si no hay una conversación
            activa entonces se guardará en el historial inicial.
            Caso contrario se guardará en el historial actual.
        """
        pass
    
    def clearHistory(self):
        """
            Borra todos los mensajes tanto del historial inicial, como del actual y borra
            la conversación activa.
        """
        pass
        
    def sendMessage(self, message: str) -> str:
        """
            Envía un mensaje a la IA y lo guarda en el historial actual, teniendo como mensajes
            previos el historial inicial y actual.
        """
        pass

    def getMessage(self, indx: int) -> str:
        """
            Regresa un mensaje del historial dado su índice. El historial inicial y actual están
            unidos.
        """
        pass