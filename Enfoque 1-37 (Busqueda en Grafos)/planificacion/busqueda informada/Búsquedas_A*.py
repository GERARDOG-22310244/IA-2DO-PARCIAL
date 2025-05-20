import heapq

# Grafo con costos
grafo = {
    'A': {'B': 1, 'C': 4},
    'B': {'D': 2, 'E': 5},
    'C': {'F': 3},
    'D': {},
    'E': {'F': 1},
    'F': {}
}

# Heurísticas hacia el nodo objetivo F
heuristica = {
    'A': 7,
    'B': 6,
    'C': 4,
    'D': 4,
    'E': 2,
    'F': 0
}

def busqueda_a_estrella(inicio, objetivo):
    frontera = []
    heapq.heappush(frontera, (heuristica[inicio], 0, [inicio]))

    visitados = {}

    while frontera:
        f, costo_actual, camino = heapq.heappop(frontera)
        nodo = camino[-1]

        if nodo == objetivo:
            return camino

        if nodo in visitados and visitados[nodo] <= costo_actual:
            continue
        visitados[nodo] = costo_actual

        for vecino, costo in grafo[nodo].items():
            nuevo_costo = costo_actual + costo
            nueva_f = nuevo_costo + heuristica[vecino]
            nuevo_camino = camino + [vecino]
            heapq.heappush(frontera, (nueva_f, nuevo_costo, nuevo_camino))

    return None

# Prueba de A*
resultado = busqueda_a_estrella('A', 'F')
print("Camino encontrado con A*:", " -> ".join(resultado))
