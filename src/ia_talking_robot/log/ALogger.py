import string

class ALogger:

    def __init__(self, useTimeStamp : bool = True, excludedLevels = []):
        self.useTimeStamp = useTimeStamp;
        self.excludedLevels = excludedLevels
        pass

    # Abstract Method
    def logMessage(self, message : string, level = 0, caller : string = None):
        pass


    def setTimeStamp(self, value: bool):
        self.useTimeStamp = value
        pass

    def excludeLevel(self, level: int):
        if level in self.excludedLevels:
            return
        self.excludedLevels.append(level)      
        

    def includeLevel(self, level: int):
        if level in self.excludedLevels:
            self.excludedLevels.remove(level)
        