from typing import List

from .ALogger import ALogger
from .LogLevel import LogLevel
class CLoggableObject:
    
    def __init__(self):
        self.loggers : List[ALogger] = []
        self.name = ""
        
    def addNewLogger(self, logger : ALogger):
        self.loggers.append(logger)

    def logMessage(self, message : str, level = LogLevel.INFO):
        for logger in self.loggers:
            if self.name != "":
                logger.logMessage(message, level, f"{self.name}" )
            else:
                logger.logMessage(message, level, f"{self.__class__.__name__}")

    def DEBUG(self, message : str):
        self.logMessage(message, LogLevel.INFO)

    def LOG(self, message : str):
        self.logMessage(message, LogLevel.MESSAGE)

    def WARNING(self, message : str):
        self.logMessage(message, LogLevel.WARNING)

    def ERROR(self, message : str):
        self.logMessage(message, LogLevel.ERROR)

    def setNameOnLog(self, name : str):
        self.name = name

