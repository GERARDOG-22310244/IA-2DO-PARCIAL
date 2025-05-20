# Grafo representado como un diccionario
grafo = {
    'A': ['B', 'C'],
    'B': ['D', 'E'],
    'C': ['F'],
    'D': [],
    'E': ['F'],
    'F': []
}

# Función de búsqueda en profundidad limitada
def dfs_limitado(nodo, objetivo, limite, camino, visitados):
    if nodo == objetivo:
        return camino + [nodo]
    if limite <= 0:
        return None

    visitados.add(nodo)
    for vecino in grafo.get(nodo, []):
        if vecino not in visitados:
            resultado = dfs_limitado(vecino, objetivo, limite - 1, camino + [nodo], visitados.copy())
            if resultado:
                return resultado
    return None

# Función de búsqueda en profundidad iterativa
def iddfs(inicio, objetivo, profundidad_max):
    for limite in range(profundidad_max + 1):
        resultado = dfs_limitado(inicio, objetivo, limite, [], set())
        if resultado:
            return resultado
    return None

# Ejecutar la búsqueda
inicio = 'A'
objetivo = 'F'
profundidad_maxima = 5

camino = iddfs(inicio, objetivo, profundidad_maxima)

# Mostrar resultados
if camino:
    print(f"Camino encontrado de {inicio} a {objetivo}: {' -> '.join(camino)}")
else:
    print("No se encontró un camino.")
