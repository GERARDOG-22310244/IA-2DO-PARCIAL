# Diccionario que representa el mapa (grafo) de Australia
mapa = {
    'WA': ['NT', 'SA'],
    'NT': ['WA', 'SA', 'Q'],
    'SA': ['WA', 'NT', 'Q', 'NSW', 'V'],
    'Q': ['NT', 'SA', 'NSW'],
    'NSW': ['SA', 'Q', 'V'],
    'V': ['SA', 'NSW', 'T'],
    'T': ['V']
}

# Colores posibles
colores = ['Rojo', 'Verde', 'Azul']

# Asignación inicial vacía
asignacion = {}

# Función para comprobar si un color es válido para una región
def es_valido(region, color):
    for vecina in mapa[region]:
        if vecina in asignacion and asignacion[vecina] == color:
            return False
    return True

# Búsqueda por vuelta atrás (backtracking)
def resolver(region_index=0, regiones=list(mapa.keys())):
    if region_index == len(regiones):
        return True

    region = regiones[region_index]
    for color in colores:
        if es_valido(region, color):
            asignacion[region] = color
            if resolver(region_index + 1, regiones):
                return True
            del asignacion[region]  # deshacer si no funciona
    return False

# Ejecutar la búsqueda
if resolver():
    print("Solución encontrada:")
    for region in asignacion:
        print(f"{region} → {asignacion[region]}")
else:
    print("No se encontró solución válida.")
