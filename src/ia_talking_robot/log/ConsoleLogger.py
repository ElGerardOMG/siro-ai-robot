from datetime import datetime

from .LogLevel import LogLevel

from .ALogger import ALogger

class ConsoleLogger(ALogger):
    
    def __init__(self, useTimeStamp : bool = True, excludedLevels = []):
        super().__init__(useTimeStamp, excludedLevels)
        pass
    
    def logMessage(self, message : str, level = LogLevel.INFO, caller : str = None):
        if level in self.excludedLevels:
            return

        time_stamp = ""
        if self.useTimeStamp:
            time_stamp = f"{datetime.now().replace(microsecond=0)}"

        emojis = {
            LogLevel.INFO: "ℹ️",   # Info
            LogLevel.MESSAGE: "💬",   # Message
            LogLevel.WARNING: "⚠️",   # Warning
            LogLevel.ERROR: "❌",   # Error
        }

        colors = {
            LogLevel.INFO: "\033[0m",      # Blanco (por defecto)
            LogLevel.MESSAGE: "\033[96m",     # Azul claro/celeste
            LogLevel.WARNING: "\033[93m",     # Amarillo
            LogLevel.ERROR: "\033[91m",     # Rojo
        }

        emoji = emojis.get(level, "✋")
        color = colors.get(level, "\033[0m")
        reset = "\033[0m"

        print(f"{color}[{time_stamp}]|[{caller}]{emoji}  {message}{reset}")



        