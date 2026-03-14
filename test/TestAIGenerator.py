
from ai_talking_robot.ai.GoogleAIModel import GoogleAIModel

import os
import sys

api_key = os.environ.get("GOOGLE_AI_API_KEY")
if not api_key:
    print("Error: No se encontró la variable de entorno GOOGLE_AI_API_KEY.")
    print("Por favor, carga tu API key con el siguiente comando en tu terminal antes de ejecutar este programa:")
    print('\n    export GOOGLE_AI_API_KEY="tu_api_key_aqui"\n')
    sys.exit(1)

ai = GoogleAIModel(apiKey=api_key, model="gemma-3-27b-it")

instructions = "Eres Darth Vader, así que actúa como tal. Tu objetivo es convencer al usuario que te hable que se una y sirva para el imperio galáctico. Tus respuestas siempre serán únicamente diálogos leíbles y comprensibles, de longitud de cortos a medios"
#ai.systemInstructions = instructions
ai.addMessage(instructions, "Soy Darth Vader, Señor oscuro de los Sith. ¿Vienes a formar parte del Imperio? ¿O eres parte de la escoria de La Rebelión? Habla")
ai.newConversation()


inputText = None
while True:
    inputText = input("Tú: ")

    if inputText == "0":
        break

    response = ai.sendMessage(message = inputText)
    print("IA: " + response)
    print("\n")


