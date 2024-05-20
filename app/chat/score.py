"""
Este módulo define funciones para gestionar los componentes del chat basados en sus puntuaciones almacenadas en Redis.
Incluye funciones para seleccionar un componente aleatorio ponderado por su puntuación, actualizar las puntuaciones de una conversación, 
y obtener las puntuaciones promedio de los componentes.
"""

from app.chat.redis import client
import random

def random_component_by_score(component_type, component_map):
    # Asegura que el tipo de componente sea 'llm', 'retriever' o 'memory'
    if component_type not in ["llm", "retriever", "memory"]:
        raise ValueError("Invalid component_type")

    # Obtiene desde Redis el hash que contiene las puntuaciones totales de los componentes
    values = client.hgetall(f"{component_type}_score_values")
    # Obtiene desde Redis el hash que contiene la cantidad de votos de los componentes
    counts = client.hgetall(f"{component_type}_score_counts")

    # Obtiene todos los nombres de componentes válidos desde el mapa de componentes
    names = component_map.keys()

    # Calcula la puntuación promedio para cada componente y la agrega a un diccionario
    avg_scores = {}
    for name in names:
        score = int(values.get(name, 1))
        count = int(counts.get(name, 1))
        avg = score / count
        avg_scores[name] = max(avg, 0.1)

    # Selección aleatoria ponderada por la puntuación promedio
    sum_scores = sum(avg_scores.values())
    random_val = random.uniform(0, sum_scores)
    cumulative = 0
    for name, score in avg_scores.items():
        cumulative += score
        if random_val <= cumulative:
            return name

def score_conversation(
    conversation_id: str, score: float, llm: str, retriever: str, memory: str
) -> None:
    # Asegura que la puntuación esté entre 0 y 1
    score = min(max(score, 0), 1)

    client.hincrby("llm_score_values", llm, score)
    client.hincrby("llm_score_counts", llm, 1)

    client.hincrby("retriever_score_values", retriever, score)
    client.hincrby("retriever_score_counts", retriever, 1)

    client.hincrby("memory_score_values", memory, score)
    client.hincrby("memory_score_counts", memory, 1)

def get_scores():
    aggregate = {"llm": {}, "retriever": {}, "memory": {}}

    for component_type in aggregate.keys():
        values = client.hgetall(f"{component_type}_score_values")
        counts = client.hgetall(f"{component_type}_score_counts")

        names = values.keys()

        for name in names:
            score = int(values.get(name, 1))
            count = int(counts.get(name, 1))
            avg = score / count 
            aggregate[component_type][name] = [avg]

    return aggregate
