# Grafo representado como un diccionario de adyacencias
grafo = {
    'A': ['B', 'C'],
    'B': ['A', 'C', 'D'],
    'C': ['A', 'B', 'D'],
    'D': ['B', 'C']
}

# Lista de colores disponibles
colores = ['Rojo', 'Verde', 'Azul']

# Asignación de colores a los nodos
asignacion = {}

# Verifica si el color puede ser asignado al nodo sin conflictos
def es_valido(nodo, color):
    for vecino in grafo[nodo]:
        if vecino in asignacion and asignacion[vecino] == color:
            return False
    return True

# Algoritmo de búsqueda por vuelta atrás
def backtracking(nodo_index=0, nodos=list(grafo.keys())):
    if nodo_index == len(nodos):
        return True  # Todos los nodos fueron asignados

    nodo = nodos[nodo_index]
    for color in colores:
        if es_valido(nodo, color):
            asignacion[nodo] = color
            if backtracking(nodo_index + 1, nodos):
                return True
            del asignacion[nodo]  # Deshace la asignación si no funciona
    return False

# Ejecutar la búsqueda
if backtracking():
    print("Solución encontrada:")
    for nodo, color in asignacion.items():
        print(f"{nodo} → {color}")
else:
    print("No se encontró una solución válida.")
