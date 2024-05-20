"""
Este módulo define una función para construir un objeto de memoria de ventana de buffer de conversación utilizando LangChain.
La función `window_buffer_memory_builder` configura la memoria de la conversación con un historial de mensajes SQL y otros parámetros específicos.
"""

from langchain.memory import ConversationBufferWindowMemory
from app.chat.memories.histories.sql_history import SqlMessageHistory
# warnings_filter.py
import warnings

# Ignorar todas las advertencias de LangChain deprecado
warnings.filterwarnings("ignore", category=DeprecationWarning, module='langchain_core._api.deprecation')

def window_buffer_memory_builder(chat_args):
    """
    Construye un objeto de memoria de ventana de buffer de conversación utilizando los argumentos del chat.

    :param chat_args: Argumentos del chat que contienen el ID de la conversación y otros metadatos

    :return: Instancia de ConversationBufferWindowMemory configurada con los parámetros especificados
    """
    return ConversationBufferWindowMemory(
        memory_key="chat_history",  # Clave de la memoria del chat
        output_key="answer",  # Clave de la respuesta
        return_messages=True,  # Indicador de si se deben devolver los mensajes
        chat_memory=SqlMessageHistory(
            conversation_id=chat_args.conversation_id
        ),  # Historial de mensajes SQL para la conversación
        k=2  # Número de mensajes a mantener en la ventana de buffer
    )
