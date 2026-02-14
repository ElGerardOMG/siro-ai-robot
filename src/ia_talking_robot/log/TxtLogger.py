from datetime import datetime
import atexit

from .ALogger import ALogger

class TxtLogger(ALogger):
    
    def __init__(self, filename: str, useTimeStamp: bool = True, excludedLevels = []):
        super().__init__(useTimeStamp, excludedLevels)
        self.filename = filename
        # Abrir el archivo en modo append, lo crea si no existe
        self.file = open(self.filename, "a", encoding="utf-8")
        # Escribir la línea de encabezado con fecha y hora
        self.file.write(f"----------{datetime.now()}----------\n")
        self.file.flush()
        # Registrar el cierre automático al terminar el programa
        atexit.register(self.closeFile)
    
    def logMessage(self, message: str, level = 0, caller: str = None):
        if level in self.excludedLevels:
            return

        time_stamp = ""
        if self.useTimeStamp:
            time_stamp = f"{datetime.now()}"

        emojis = {
            0: "i",   # Info
            1: "a",   # Message
            2: "!",   # Warning
            3: "X",   # Error
        }

        emoji = emojis.get(level, "")

        self.file.write(f"[{time_stamp}]|[{caller}][{emoji}]: {message}")
        self.file.flush()
    
    def closeFile(self):
        if not self.file.closed:
            self.file.close()
