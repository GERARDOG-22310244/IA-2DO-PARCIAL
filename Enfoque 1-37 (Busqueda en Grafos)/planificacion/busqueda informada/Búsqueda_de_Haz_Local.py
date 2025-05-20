import heapq

# Grafo con conexiones y costos
grafo = {
    'A': [('B', 1), ('C', 4)],
    'B': [('D', 1), ('E', 3)],
    'C': [('F', 5)],
    'D': [('G', 1)],
    'E': [('G', 2)],
    'F': [('G', 1)],
    'G': []
}

# Heurística: estimación del costo al objetivo
heuristica = {
    'A': 6,
    'B': 4,
    'C': 5,
    'D': 3,
    'E': 2,
    'F': 4,
    'G': 0
}

def obtener_vecinos(nodo):
    return grafo.get(nodo, [])

def evaluar_camino(camino):
    return heuristica[camino[-1]]

def busqueda_haz_local(inicio, objetivo, k=2, max_iter=20):
    haz = [[inicio]]  # Lista de caminos actuales

    for _ in range(max_iter):
        todos_los_vecinos = []

        for camino in haz:
            ultimo = camino[-1]
            if ultimo == objetivo:
                return camino

            for vecino, _ in obtener_vecinos(ultimo):
                nuevo_camino = camino + [vecino]
                heapq.heappush(todos_los_vecinos, (evaluar_camino(nuevo_camino), nuevo_camino))

        # Elegimos los k mejores caminos basados en heurística
        haz = [heapq.heappop(todos_los_vecinos)[1] for _ in range(min(k, len(todos_los_vecinos)))]

    return None

# Ejecutar búsqueda
resultado = busqueda_haz_local('A', 'G', k=2)
if resultado:
    print("Camino encontrado con Búsqueda de Haz Local:", " -> ".join(resultado))
else:
    print("No se encontró un camino al objetivo.")
