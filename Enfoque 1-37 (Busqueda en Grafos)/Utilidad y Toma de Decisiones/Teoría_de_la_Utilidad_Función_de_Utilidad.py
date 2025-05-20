import heapq

# Grafo ponderado con (costo, riesgo)
grafo = {
    'A': {'B': (3, 0.1), 'C': (2, 0.3)},
    'B': {'D': (4, 0.2)},
    'C': {'D': (2, 0.4)},
    'D': {'E': (3, 0.1)},
    'E': {}
}

# Función de utilidad: penaliza costo y riesgo
def funcion_utilidad(costo, riesgo, alfa=1.0, beta=5.0):
    return -(alfa * costo + beta * riesgo)

# Algoritmo: Búsqueda basada en utilidad máxima (Dijkstra con utilidad)
def busqueda_utilidad_max(grafo, inicio, fin):
    heap = [(-0, inicio, [], 0, 0)]  # utilidad_negativa, nodo, camino, costo, riesgo
    visitados = set()

    while heap:
        utilidad_neg, nodo, camino, costo_total, riesgo_total = heapq.heappop(heap)
        if nodo in visitados:
            continue
        visitados.add(nodo)
        camino = camino + [nodo]

        if nodo == fin:
            return {
                'camino': camino,
                'costo': costo_total,
                'riesgo': riesgo_total,
                'utilidad': -utilidad_neg
            }

        for vecino, (costo, riesgo) in grafo[nodo].items():
            nuevo_costo = costo_total + costo
            nuevo_riesgo = riesgo_total + riesgo
            utilidad = funcion_utilidad(nuevo_costo, nuevo_riesgo)
            heapq.heappush(heap, (utilidad, vecino, camino, nuevo_costo, nuevo_riesgo))

    return None

# Ejecutar búsqueda
resultado = busqueda_utilidad_max(grafo, 'A', 'E')

# Mostrar resultado
if resultado:
    print("Camino óptimo:", " → ".join(resultado['camino']))
    print("Costo total:", resultado['costo'])
    print("Riesgo total:", resultado['riesgo'])
    print("Utilidad total:", resultado['utilidad'])
else:
    print("No se encontró un camino.")
