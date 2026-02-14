"""
from google import genai
from google.genai import types

client = genai.Client(api_key="AIzaSyASJp6_TqFG10zRb2ORqoF6qbUM4Q4EKMI")


chat = client.chats.create(
    model="gemini-2.0-flash-lite",
    config=types.GenerateContentConfig(
        system_instruction="Eres Darth Vader, así que actúa como tal. Tu objetivo es convencer al usuario que te hable que se una y sirva para el imperio galáctico. Tus respuestas siempre serán únicamente diálogos leíbles y comprensibles"),
    history=[
        types.Content(role="user", parts=[types.Part(text="...")]),
        types.Content(
            role="model",
            parts=[
                types.Part(
                    text="Soy Darth Vader, Señor Oscuro de los Sith. Dime ¿Vienes a formar parte del imperio?"
                )
            ],
        ),
    ],

)

nuevo_mensaje = "Mi nombre es Juan, soy eléctrico. No sé si eso sirva"
response = chat.send_message(message = nuevo_mensaje)
# Agregar el nuevo mensaje al historial

# Imprimir la respuesta
print(response)
print(response.text)
# Para la siguiente interacción, agrega la respuesta del modelo al historial:

# Ahora `conversacion` contiene todo el historial.
"""

from src.ia_talking_robot.ai.GoogleAIModel import GoogleAIModel

ai = GoogleAIModel(apiKey="AIzaSyASJp6_TqFG10zRb2ORqoF6qbUM4Q4EKMI", model="gemini-2.0-flash-lite")
ai.setInstructions("Eres Darth Vader, así que actúa como tal. Tu objetivo es convencer al usuario que te hable que se una y sirva para el imperio galáctico. Tus respuestas siempre serán únicamente diálogos leíbles y comprensibles, de longitud de cortos a medios")
ai.addInitialMessage(role=GoogleAIModel.ROLE_MODEL, message="Soy Darth Vader, Señor Oscuro de los Sith. Dime ¿Vienes a formar parte del imperio?")
print(ai.getMessage(0))
ai.newConversation()
print(ai.getMessage(0))

try:
    response = ai.sendMessage("Me llamo Lucas, supe que el imperio buscaba nuevos miembros")
    
except Exception as e:
    print(f"Algo salió mal... {e}")

print(response)