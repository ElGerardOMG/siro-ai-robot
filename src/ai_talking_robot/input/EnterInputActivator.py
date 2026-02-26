from .AInputActivator import AInputActivator

class EnterInputActivator(AInputActivator):
    
    def __init__(self):
        pass

    def waitForInput(self):
        input()
        pass