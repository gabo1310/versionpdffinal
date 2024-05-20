"""
Este módulo define un mapa de memorias utilizando diferentes constructores de memoria.
Incluye memorias de buffer SQL y memorias de ventana de buffer SQL, cada una configurada con sus respectivos constructores.
"""

from .sql_memory import build_memory
from .window_memory import window_buffer_memory_builder

# Define un mapa de memorias con diferentes tipos de memoria y sus constructores correspondientes
memory_map = {
    "sql_buffer_memory": build_memory,  # Constructor para la memoria de buffer SQL
    "sql_window_memory": window_buffer_memory_builder  # Constructor para la memoria de ventana de buffer SQL
}
