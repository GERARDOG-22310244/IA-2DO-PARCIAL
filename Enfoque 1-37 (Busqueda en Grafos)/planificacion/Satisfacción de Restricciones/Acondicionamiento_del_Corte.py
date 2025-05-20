import itertools

# Grafo con ciclos
grafo = {
    'A': ['B', 'C'],
    'B': ['A', 'C', 'D'],
    'C': ['A', 'B', 'D'],
    'D': ['B', 'C', 'E'],
    'E': ['D']
}

colores = ['Rojo', 'Verde', 'Azul']

# Identificar un cutset (por simplicidad, elegimos manualmente)
cutset = ['B']

# Verifica si una asignación es válida
def es_valida(asignacion, grafo):
    for nodo in asignacion:
        for vecino in grafo[nodo]:
            if vecino in asignacion and asignacion[nodo] == asignacion[vecino]:
                return False
    return True

# Asignación libre sobre el árbol restante (resto del grafo)
def resolver_restante(asignacion_parcial, grafo, colores):
    nodos_restantes = [n for n in grafo if n not in asignacion_parcial]

    def backtrack(asignacion):
        if len(asignacion) == len(grafo):
            return asignacion

        for nodo in nodos_restantes:
            if nodo in asignacion:
                continue
            for color in colores:
                asignacion[nodo] = color
                if es_valida(asignacion, grafo):
                    resultado = backtrack(asignacion.copy())
                    if resultado:
                        return resultado
                del asignacion[nodo]
            return None
        return None

    return backtrack(asignacion_parcial.copy())

# Enumerar todas las asignaciones posibles del cutset
for valores in itertools.product(colores, repeat=len(cutset)):
    asignacion_cutset = dict(zip(cutset, valores))
    if not es_valida(asignacion_cutset, grafo):
        continue

    # Resolver el resto
    resultado = resolver_restante(asignacion_cutset, grafo, colores)
    if resultado:
        print("Solución encontrada:")
        for nodo, color in resultado.items():
            print(f"{nodo} → {color}")
        break
else:
    print("No se encontró una solución sin conflictos.")
