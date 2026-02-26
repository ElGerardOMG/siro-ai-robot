import socket
import json
import time
import math
from ai_talking_robot.controllers.AComponentController import AComponentController
from ai_talking_robot.sequencer.ComponentEnum import ComponentEnum

class VirtualRobotController(AComponentController):
    def __init__(self, components: type[ComponentEnum], ip="127.0.0.1", port=5005):
        self.ip = ip
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        self._components = []
        self._values = []

        for indx, component in enumerate(components):
            component.label = indx
            component.initialize(self)
            self._components.append(component)
            self._values.append(component.min_value)
            

    def setComponentValue(self, component : ComponentEnum, value):
        """
        Envía el comando al simulador visual.
        servo_name: String (ej. 'NECK_X')
        angle: Float (grados)
        """
        self._values[component.channel] = value

        payload = {
            "servo": component.name,
            "angle": value
        }
        message = json.dumps(payload).encode()
        self.sock.sendto(message, (self.ip, self.port))

    def getComponentValue(self, component: ComponentEnum):
        return self._values[component.channel]

# --- EJEMPLO DE USO (Lo que tú programarías) ---
"""
bot = VirtualRobotController()

print("Iniciando secuencia de prueba...")

# 1. Mover la cabeza (decir que No)
for i in range(-30, 30, 2):
    bot.setComponentValue("NECK_Y", i)
    time.sleep(0.05)

# 2. Levantar brazo izquierdo (Shoulder X)
print("Levantando brazo...")
for i in range(0, 90, 2):
    bot.setComponentValue("SHOULDER_L_X", i)
    time.sleep(0.02)

# 3. Saludar (Mover antebrazo/codo)
print("Saludando...")
for _ in range(3):
    for angle in range(0, 45, 5):
        bot.setComponentValue("ELBOW_L", angle)
        time.sleep(0.02)
    for angle in range(45, 0, -5):
        bot.setComponentValue("ELBOW_L", angle)
        time.sleep(0.02)

print("Prueba finalizada.")
"""