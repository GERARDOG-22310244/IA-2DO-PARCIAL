# Grafo simple para problema de coloreo
grafo = {
    'A': ['B', 'C'],
    'B': ['A', 'C', 'D'],
    'C': ['A', 'B', 'D'],
    'D': ['B', 'C']
}

colores = ['Rojo', 'Verde', 'Azul']

# Verificar si la asignación es válida
def es_valido(nodo, color, asignacion):
    for vecino in grafo[nodo]:
        if vecino in asignacion and asignacion[vecino] == color:
            return False
    return True

# Backjumping dirigido por conflictos
def cbj(nodos, asignacion={}, conflicto={}):
    if len(asignacion) == len(nodos):
        return asignacion

    nodo = siguiente_variable(asignacion, nodos)
    for color in colores:
        if es_valido(nodo, color, asignacion):
            asignacion[nodo] = color
            conflicto[nodo] = set()
            resultado = cbj(nodos, asignacion.copy(), conflicto)
            if resultado:
                return resultado
        else:
            # Registrar conflicto
            for vecino in grafo[nodo]:
                if vecino in asignacion and asignacion[vecino] == color:
                    if nodo not in conflicto:
                        conflicto[nodo] = set()
                    conflicto[nodo].add(vecino)

    # Salto atrás dirigido por conflictos
    if nodo in conflicto and conflicto[nodo]:
        variable_conflicto = max(conflicto[nodo], key=lambda x: nodos.index(x))
        # Borrar asignaciones posteriores al conflicto
        for var in list(asignacion):
            if nodos.index(var) >= nodos.index(variable_conflicto):
                del asignacion[var]
        return cbj(nodos, asignacion.copy(), conflicto)

    return None

# Selección simple del siguiente nodo no asignado
def siguiente_variable(asignacion, nodos):
    for n in nodos:
        if n not in asignacion:
            return n

# Ejecutar el algoritmo
nodos = list(grafo.keys())
resultado = cbj(nodos)

if resultado:
    print("Asignación válida encontrada:")
    for nodo, color in resultado.items():
        print(f"{nodo} → {color}")
else:
    print("No se encontró una asignación válida.")
