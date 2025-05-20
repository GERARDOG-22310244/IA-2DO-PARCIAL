# Estructura de grafo AND-OR: cada nodo tiene varias opciones (OR), y cada opción puede ser un conjunto de nodos (AND)
grafo_ao = {
    'A': [[('B', 1)], [('C', 1), ('D', 1)]],  # A -> B (OR) o C y D (AND)
    'B': [[('E', 1)]],
    'C': [[('F', 1)]],
    'D': [[('F', 1)]],
    'E': [],
    'F': []
}

# Heurística estimada al objetivo
heuristica_ao = {
    'A': 3,
    'B': 2,
    'C': 2,
    'D': 2,
    'E': 0,
    'F': 0
}

solucion = {}

def ao_star(nodo):
    if nodo not in grafo_ao or not grafo_ao[nodo]:
        solucion[nodo] = []
        return 0

    menor_costo = float('inf')
    mejor_opcion = None

    for opcion in grafo_ao[nodo]:
        costo = 0
        for hijo, peso in opcion:
            costo += peso + heuristica_ao[hijo]
        if costo < menor_costo:
            menor_costo = costo
            mejor_opcion = opcion

    solucion[nodo] = mejor_opcion

    for hijo, _ in mejor_opcion:
        ao_star(hijo)

    return menor_costo

# Ejecutar AO*
ao_star('A')
print("Solución AO*:")
for k, v in solucion.items():
    print(f"{k} -> {[n for n, _ in v]}")
