import os
from dotenv import load_dotenv
import anthropic

# Cargar las variables de entorno del archivo .env
load_dotenv()

# Crear un cliente de Anthropic usando la clave API del entorno
client = anthropic.Anthropic(
    api_key=os.getenv("ANTHROPIC_API_KEY")  # Obtiene la clave API de las variables de entorno
)

message = client.messages.create(
    model="claude-3-opus-20240229",
    max_tokens=1024,
    messages=[
        {"role": "user", "content": "Hello, Claude, en español"}
    ]
)
print(message.content)

