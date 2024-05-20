"""
Este módulo define una función para construir un modelo de lenguaje (LLM) utilizando LangChain y Anthropic.
La función `build_llm_clau` configura el modelo de lenguaje con los parámetros proporcionados, incluyendo el nombre del modelo y si se debe utilizar el streaming.
Verifica que la clave API de Anthropic esté configurada en las variables de entorno.
"""

import os
from langchain_anthropic import ChatAnthropic
# warnings_filter.py
import warnings

# Ignorar todas las advertencias de LangChain deprecado
warnings.filterwarnings("ignore", category=DeprecationWarning, module='langchain_core._api.deprecation')

def build_llm_clau(chat_args, model_name):
    """
    Construye un modelo de lenguaje (LLM) utilizando los argumentos del chat y Anthropic.

    :param chat_args: Argumentos del chat que contienen el ID de la conversación y otros metadatos
    :param model_name: Nombre del modelo de lenguaje a utilizar

    :return: Instancia de ChatAnthropic configurada con los parámetros especificados

    :raises ValueError: Si la clave API de Anthropic no está configurada en las variables de entorno
    """
    api_key = os.getenv('ANTHROPIC_API_KEY')  # Obtiene la clave API de Anthropic desde las variables de entorno

    if api_key is None:
        raise ValueError("API key is not set in the environment variables.")  # Lanza una excepción si la clave API no está configurada

    return ChatAnthropic(
        streaming=chat_args.streaming,  # Configura si el modelo debe utilizar el streaming
        model_name=model_name  # Nombre del modelo de lenguaje
    )
