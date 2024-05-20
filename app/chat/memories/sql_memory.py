"""
Este módulo define una función para construir un objeto de memoria de buffer de conversación utilizando LangChain.
La función `build_memory` configura la memoria de la conversación con un historial de mensajes SQL y otros parámetros específicos.
"""

from langchain.memory import ConversationBufferMemory
from app.chat.memories.histories.sql_history import SqlMessageHistory
# warnings_filter.py
import warnings

# Ignorar todas las advertencias de LangChain deprecado
warnings.filterwarnings("ignore", category=DeprecationWarning, module='langchain_core._api.deprecation')

def build_memory(chat_args):
    """
    Construye un objeto de memoria de buffer de conversación utilizando los argumentos del chat.

    :param chat_args: Argumentos del chat que contienen el ID de la conversación y otros metadatos

    :return: Instancia de ConversationBufferMemory configurada con los parámetros especificados
    """
    return ConversationBufferMemory(
        chat_memory=SqlMessageHistory(
            conversation_id=chat_args.conversation_id
        ),  # Historial de mensajes SQL para la conversación
        return_messages=True,  # Indicador de si se deben devolver los mensajes
        memory_key="chat_history",  # Clave de la memoria del chat
        output_key="answer"  # Clave de la respuesta
    )
