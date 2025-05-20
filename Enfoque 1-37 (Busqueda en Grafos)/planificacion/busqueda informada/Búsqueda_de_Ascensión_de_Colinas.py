# Grafo con vecinos y heurísticas (valor estimado al objetivo)
grafo = {
    'A': [('B', 3), ('C', 4)],
    'B': [('D', 2), ('E', 1)],
    'C': [('F', 6)],
    'D': [],
    'E': [],
    'F': []
}

# Heurísticas de cada nodo al objetivo final
heuristica = {
    'A': 5,
    'B': 3,
    'C': 4,
    'D': 2,
    'E': 0,  # Nodo objetivo (mejor heurística)
    'F': 6
}

def ascension_colinas(inicio):
    actual = inicio
    camino = [actual]

    while True:
        vecinos = grafo.get(actual, [])
        if not vecinos:
            break

        # Elegir el vecino con mejor heurística (más baja)
        mejor_vecino = min(vecinos, key=lambda x: heuristica[x[0]])
        
        if heuristica[mejor_vecino[0]] < heuristica[actual]:
            actual = mejor_vecino[0]
            camino.append(actual)
        else:
            # No hay mejor vecino (óptimo local)
            break

    return camino

# Ejecutar
camino_resultado = ascension_colinas('A')
print("Camino encontrado con ascensión de colinas:", " -> ".join(camino_resultado))
