import random

# Definimos el grafo
grafo = {
    'A': ['B', 'C'],
    'B': ['A', 'C', 'D'],
    'C': ['A', 'B', 'D'],
    'D': ['B', 'C']
}

colores = ['Rojo', 'Verde', 'Azul']
max_intentos = 1000

# Inicialización aleatoria
def inicializar_asignacion(grafo, colores):
    return {nodo: random.choice(colores) for nodo in grafo}

# Contar conflictos de un nodo
def contar_conflictos(nodo, color, asignacion, grafo):
    return sum(1 for vecino in grafo[nodo] if asignacion.get(vecino) == color)

# Encontrar nodo con conflictos
def obtener_nodos_con_conflictos(asignacion, grafo):
    return [
        nodo for nodo in grafo
        if any(asignacion[nodo] == asignacion.get(vecino) for vecino in grafo[nodo])
    ]

# Algoritmo de Mínimos Conflictos
def min_conflicts(grafo, colores, max_intentos=1000):
    asignacion = inicializar_asignacion(grafo, colores)

    for intento in range(max_intentos):
        conflictos = obtener_nodos_con_conflictos(asignacion, grafo)
        if not conflictos:
            return asignacion

        nodo = random.choice(conflictos)

        # Elegir el color que minimice los conflictos
        mejor_color = min(
            colores,
            key=lambda color: contar_conflictos(nodo, color, asignacion, grafo)
        )

        asignacion[nodo] = mejor_color

    return None  # No se encontró solución en los intentos dados

# Ejecutar
resultado = min_conflicts(grafo, colores, max_intentos)

if resultado:
    print("Solución encontrada:")
    for nodo, color in resultado.items():
        print(f"{nodo} → {color}")
else:
    print("No se encontró una solución sin conflictos.")
