import math
import random

# Grafo como diccionario de adyacencia con costos
grafo = {
    'A': [('B', 3), ('C', 4)],
    'B': [('D', 2), ('E', 1)],
    'C': [('F', 6)],
    'D': [('G', 1)],
    'E': [('G', 0)],
    'F': [('G', 5)],
    'G': []
}

# Heurística (puede ser distancia al objetivo estimada)
heuristica = {
    'A': 6,
    'B': 4,
    'C': 5,
    'D': 3,
    'E': 1,
    'F': 6,
    'G': 0
}

def obtener_vecinos(nodo):
    return [n for n, _ in grafo.get(nodo, [])]

def costo(nodo):
    return heuristica[nodo]

def temple_simulado(inicio, objetivo, temperatura_inicial=1000, enfriamiento=0.95, iteraciones=100):
    actual = inicio
    camino = [actual]
    mejor = actual
    t = temperatura_inicial

    for _ in range(iteraciones):
        if actual == objetivo:
            break

        vecinos = obtener_vecinos(actual)
        if not vecinos:
            break

        siguiente = random.choice(vecinos)
        delta = costo(actual) - costo(siguiente)

        if delta > 0:
            actual = siguiente
            camino.append(actual)
        else:
            prob = math.exp(delta / t)
            if random.random() < prob:
                actual = siguiente
                camino.append(actual)

        t *= enfriamiento

    return camino

# Ejecutar búsqueda
camino = temple_simulado('A', 'G')
print("Camino encontrado con Temple Simulado:", " -> ".join(camino))
