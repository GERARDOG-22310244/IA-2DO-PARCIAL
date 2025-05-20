import heapq

# Grafo con costos de los arcos
grafo = {
    'A': {'B': 1, 'C': 4},
    'B': {'D': 2, 'E': 5},
    'C': {'F': 3},
    'D': {},
    'E': {'F': 1},
    'F': {}
}

# Heurísticas estimadas desde cada nodo al nodo objetivo 'F'
heuristica = {
    'A': 7,
    'B': 6,
    'C': 4,
    'D': 4,
    'E': 2,
    'F': 0
}

# Función del algoritmo A*
def a_estrella(inicio, objetivo):
    cola_prioridad = []
    heapq.heappush(cola_prioridad, (0 + heuristica[inicio], 0, inicio, [inicio]))

    visitados = set()

    while cola_prioridad:
        f, costo_g, nodo_actual, camino = heapq.heappop(cola_prioridad)

        if nodo_actual in visitados:
            continue
        visitados.add(nodo_actual)

        if nodo_actual == objetivo:
            return camino, costo_g

        for vecino, costo in grafo.get(nodo_actual, {}).items():
            if vecino not in visitados:
                g_nuevo = costo_g + costo
                f_nuevo = g_nuevo + heuristica[vecino]
                heapq.heappush(cola_prioridad, (f_nuevo, g_nuevo, vecino, camino + [vecino]))

    return None, float('inf')

# Ejecutar búsqueda A*
inicio = 'A'
objetivo = 'F'

camino, costo_total = a_estrella(inicio, objetivo)

# Mostrar resultados
if camino:
    print(f"Camino encontrado de {inicio} a {objetivo}: {' -> '.join(camino)} con costo total: {costo_total}")
else:
    print("No se encontró un camino.")
