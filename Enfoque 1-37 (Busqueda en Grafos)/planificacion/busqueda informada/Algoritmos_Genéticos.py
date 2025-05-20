import random

# Grafo representado como diccionario
grafo = {
    'A': ['B', 'C'],
    'B': ['A', 'D', 'E'],
    'C': ['A', 'F'],
    'D': ['B', 'G'],
    'E': ['B', 'G'],
    'F': ['C', 'G'],
    'G': ['D', 'E', 'F']
}

inicio = 'A'
objetivo = 'G'
tam_poblacion = 6
max_generaciones = 20
longitud_max = 6
prob_mutacion = 0.2

# Generar individuo (camino aleatorio desde el inicio)
def generar_individuo():
    camino = [inicio]
    actual = inicio
    while actual != objetivo and len(camino) < longitud_max:
        vecinos = grafo[actual]
        siguiente = random.choice(vecinos)
        if siguiente not in camino:  # evitar ciclos
            camino.append(siguiente)
            actual = siguiente
    return camino

# Evaluar individuo (fitness: mientras más corto y llegue a objetivo, mejor)
def fitness(camino):
    if camino[-1] != objetivo:
        return 0  # penaliza si no llega
    return 1 / len(camino)  # camino más corto tiene mejor fitness

# Cruce entre dos caminos
def cruzar(p1, p2):
    punto = random.randint(1, min(len(p1), len(p2)) - 1)
    hijo = p1[:punto]
    for nodo in p2:
        if nodo not in hijo:
            hijo.append(nodo)
        if nodo == objetivo:
            break
    return hijo

# Mutación: cambiar un nodo del camino
def mutar(camino):
    if len(camino) < 2:
        return camino
    idx = random.randint(1, len(camino) - 2)
    vecinos = grafo[camino[idx - 1]]
    nuevo = random.choice(vecinos)
    nuevo_camino = camino[:idx] + [nuevo]
    actual = nuevo
    while actual != objetivo and len(nuevo_camino) < longitud_max:
        vecinos = grafo[actual]
        siguiente = random.choice(vecinos)
        if siguiente not in nuevo_camino:
            nuevo_camino.append(siguiente)
            actual = siguiente
    return nuevo_camino

# Algoritmo genético
def algoritmo_genetico():
    poblacion = [generar_individuo() for _ in range(tam_poblacion)]

    for generacion in range(max_generaciones):
        poblacion.sort(key=fitness, reverse=True)
        if fitness(poblacion[0]) > 0:
            return poblacion[0]

        nueva_poblacion = poblacion[:2]  # elitismo

        while len(nueva_poblacion) < tam_poblacion:
            padres = random.sample(poblacion[:4], 2)
            hijo = cruzar(padres[0], padres[1])
            if random.random() < prob_mutacion:
                hijo = mutar(hijo)
            nueva_poblacion.append(hijo)

        poblacion = nueva_poblacion

    return None

# Ejecutar
camino_optimo = algoritmo_genetico()
if camino_optimo:
    print("Camino encontrado con algoritmo genético:", " -> ".join(camino_optimo))
else:
    print("No se encontró un camino al objetivo.")
