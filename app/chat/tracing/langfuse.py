"""
Este módulo inicializa el cliente Langfuse utilizando 
las claves pública y secreta proporcionadas en las variables de entorno.
Configura el cliente para conectarse al host de Langfuse.
"""

import os
from langfuse.client import Langfuse
# warnings_filter.py
import warnings

# Ignorar todas las advertencias de LangChain deprecado
warnings.filterwarnings("ignore", category=DeprecationWarning, module='langchain_core._api.deprecation')

# Inicializa el cliente Langfuse utilizando las claves pública y secreta desde las variables de entorno
langfuse = Langfuse(
    os.environ["LANGFUSE_PUBLIC_KEY"],
    os.environ["LANGFUSE_SECRET_KEY"],
    host="https://cloud.langfuse.com"
)
