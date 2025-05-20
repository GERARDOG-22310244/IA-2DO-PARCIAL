import heapq

# Definimos el grafo como un diccionario
grafo = {
    'A': ['B', 'C'],
    'B': ['D', 'E'],
    'C': ['F'],
    'D': [],
    'E': ['F'],
    'F': []
}

# Heurística estimada desde cada nodo al nodo objetivo 'F'
heuristica = {
    'A': 7,
    'B': 6,
    'C': 4,
    'D': 4,
    'E': 2,
    'F': 0
}

def busqueda_voraz(inicio, objetivo):
    cola_prioridad = []
    heapq.heappush(cola_prioridad, (heuristica[inicio], [inicio]))
    visitados = set()

    while cola_prioridad:
        _, camino = heapq.heappop(cola_prioridad)
        nodo_actual = camino[-1]

        if nodo_actual in visitados:
            continue
        visitados.add(nodo_actual)

        if nodo_actual == objetivo:
            return camino

        for vecino in grafo.get(nodo_actual, []):
            if vecino not in visitados:
                nuevo_camino = camino + [vecino]
                heapq.heappush(cola_prioridad, (heuristica[vecino], nuevo_camino))

    return None

# Ejecutar búsqueda
inicio = 'A'
objetivo = 'F'

resultado = busqueda_voraz(inicio, objetivo)

# Mostrar resultados
if resultado:
    print(f"Camino encontrado con búsqueda voraz: {' -> '.join(resultado)}")
else:
    print("No se encontró un camino.")
