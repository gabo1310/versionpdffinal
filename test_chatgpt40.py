import os
from dotenv import load_dotenv
import openai

# Carga las variables de entorno desde el archivo .env
load_dotenv()

# Obtiene la API key de las variables de entorno
api_key = os.getenv("OPENAI_API_KEY")

# Configura la API key de OpenAI
openai.api_key = api_key

# Resto del código para enviar una solicitud al modelo y obtener una respuesta
response = openai.ChatCompletion.create(
    model="gpt-4o",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "que es una integral? "},
    ]
)

print(response['choices'][0]['message']['content'])
