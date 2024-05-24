"""
Este módulo inicializa el cliente Redis utilizando la URL 
proporcionada en las variables de entorno.
Configura el cliente Redis para decodificar
las respuestas automáticamente.
"""

import os
import redis
import warnings

# Ignorar todas las advertencias de LangChain deprecado
warnings.filterwarnings("ignore", category=DeprecationWarning, module='langchain_core._api.deprecation')


# Inicializa el cliente Redis utilizando la URL de Redis desde las variables de entorno
client = redis.Redis.from_url(
    os.environ["REDIS_URI"],
    decode_responses=True  # Configura el cliente para decodificar las respuestas automáticamente
)
