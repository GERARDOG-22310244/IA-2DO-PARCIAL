import random

# Definimos un grafo simple como diccionario de adyacencia con costos heurísticos
grafo = {
    'A': [('B', 3), ('C', 4)],
    'B': [('D', 2), ('E', 1)],
    'C': [('F', 6)],
    'D': [('G', 1)],
    'E': [('G', 0)],  # Objetivo
    'F': [('G', 5)],
    'G': []  # Nodo objetivo
}

# Heurística estimada al objetivo (valor ficticio para guiar la búsqueda)
heuristica = {
    'A': 6,
    'B': 4,
    'C': 5,
    'D': 3,
    'E': 1,
    'F': 6,
    'G': 0  # Objetivo
}

def busqueda_tabu(inicio, objetivo, max_iteraciones=10, tamanio_tabu=3):
    actual = inicio
    mejor_solucion = [actual]
    mejor_heuristica = heuristica[actual]
    lista_tabu = []

    for i in range(max_iteraciones):
        vecinos = grafo.get(actual, [])
        if not vecinos:
            break

        # Filtrar vecinos que no están en la lista tabú
        candidatos = [(nodo, heuristica[nodo]) for nodo, _ in vecinos if nodo not in lista_tabu]

        if not candidatos:
            break  # Si no hay candidatos válidos, se detiene

        # Elegir el vecino con mejor (menor) heurística
        siguiente, h = min(candidatos, key=lambda x: x[1])

        # Actualizar la lista tabú
        lista_tabu.append(actual)
        if len(lista_tabu) > tamanio_tabu:
            lista_tabu.pop(0)

        # Actualizar estado
        actual = siguiente
        mejor_solucion.append(actual)
        mejor_heuristica = h

        if actual == objetivo:
            break

    return mejor_solucion

# Ejecutar la búsqueda Tabú
camino = busqueda_tabu('A', 'G', max_iteraciones=10, tamanio_tabu=3)
print("Camino encontrado con Búsqueda Tabú:", " -> ".join(camino))

