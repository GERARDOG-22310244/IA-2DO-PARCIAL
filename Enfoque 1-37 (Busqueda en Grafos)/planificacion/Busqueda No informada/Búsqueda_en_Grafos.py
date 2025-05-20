from collections import deque

# Definimos el grafo como un diccionario
grafo = {
    'A': ['B', 'C'],
    'B': ['D', 'E'],
    'C': ['F'],
    'D': [],
    'E': ['F'],
    'F': []
}

def bfs(grafo, inicio, objetivo):
    visitados = set()
    cola = deque([[inicio]])

    while cola:
        camino = cola.popleft()
        nodo = camino[-1]

        if nodo == objetivo:
            return camino

        if nodo not in visitados:
            visitados.add(nodo)
            for vecino in grafo[nodo]:
                nuevo_camino = list(camino)
                nuevo_camino.append(vecino)
                cola.append(nuevo_camino)
    
    return None

# Ejecutar la búsqueda
inicio = 'A'
objetivo = 'F'
camino_encontrado = bfs(grafo, inicio, objetivo)

if camino_encontrado:
    print(f"Camino encontrado de {inicio} a {objetivo}: {' -> '.join(camino_encontrado)}")
else:
    print("No se encontró un camino.")
