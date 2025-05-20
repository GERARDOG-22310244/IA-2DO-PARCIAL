from collections import deque

# Grafo de adyacencia
grafo = {
    'A': ['B', 'C'],
    'B': ['A', 'C', 'D'],
    'C': ['A', 'B', 'D'],
    'D': ['B', 'C']
}

# Colores posibles para cada nodo
colores = ['Rojo', 'Verde', 'Azul']

# Dominio inicial para cada nodo
dominios = {nodo: list(colores) for nodo in grafo}

# AC-3: Arc Consistency Algorithm
def ac3():
    cola = deque([(xi, xj) for xi in grafo for xj in grafo[xi]])

    while cola:
        xi, xj = cola.popleft()
        if revisar(xi, xj):
            if not dominios[xi]:
                return False
            for xk in grafo[xi]:
                if xk != xj:
                    cola.append((xk, xi))
    return True

# Revisión de consistencia entre dos nodos
def revisar(xi, xj):
    revisado = False
    for x in dominios[xi][:]:
        if not any(x != y for y in dominios[xj]):
            dominios[xi].remove(x)
            revisado = True
    return revisado

# Asignación de colores si AC-3 encuentra solución
def asignar_colores():
    if not ac3():
        print("No hay solución posible con AC-3.")
        return

    print("Solución posible (colores únicos si hay dominio de tamaño 1):")
    for nodo in dominios:
        if len(dominios[nodo]) == 1:
            print(f"{nodo} → {dominios[nodo][0]}")
        else:
            print(f"{nodo} → {dominios[nodo]} (múltiples opciones)")

# Ejecutar
asignar_colores()
