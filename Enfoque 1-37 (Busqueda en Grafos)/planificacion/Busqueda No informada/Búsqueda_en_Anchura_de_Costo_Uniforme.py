from queue import PriorityQueue
from typing import List, Dict, Set, Tuple, Optional

# Definición de tipos
Estado = str
Accion = str
ProblemaBusqueda = Dict[Estado, List[Tuple[Accion, Estado, float]]]  # Ahora incluye costo

class ProblemaPlanificacionBusqueda:
    def __init__(self, estado_inicial: Estado, estados_meta: Set[Estado], acciones: ProblemaBusqueda):
        """
        Inicializa un problema de planificación como búsqueda con costos
        
        Args:
            estado_inicial: Estado inicial del problema
            estados_meta: Conjunto de estados meta
            acciones: Diccionario de acciones por estado (con costo)
        """
        self.estado_inicial = estado_inicial
        self.estados_meta = estados_meta
        self.acciones = acciones
    
    def es_meta(self, estado: Estado) -> bool:
        """Verifica si un estado es estado meta"""
        return estado in self.estados_meta
    
    def acciones_aplicables(self, estado: Estado) -> List[Tuple[Accion, float]]:
        """Devuelve las acciones aplicables en un estado con sus costos"""
        return [(accion, costo) for accion, _, costo in self.acciones.get(estado, [])]
    
    def resultado(self, estado: Estado, accion: Accion) -> Tuple[Estado, float]:
        """Aplica una acción a un estado y devuelve el nuevo estado y su costo"""
        for a, s, c in self.acciones.get(estado, []):
            if a == accion:
                return s, c
        return estado, 0  # Si la acción no es aplicable, devuelve el mismo estado con costo 0

def busqueda_costo_uniforme(problema: ProblemaPlanificacionBusqueda) -> Optional[Tuple[List[Accion], float]]:
    """
    Implementación de búsqueda de costo uniforme para planificación
    
    Args:
        problema: Problema de planificación como búsqueda con costos
        
    Returns:
        Tupla con (lista de acciones, costo total) que llevan del estado inicial a un estado meta, 
        o None si no hay solución
    """
    # Frontera: cola de prioridad (costo acumulado, estado, camino)
    frontera = PriorityQueue()
    frontera.put((0, problema.estado_inicial, []))
    
    # Diccionario de costos mínimos conocidos para cada estado
    costos_minimos = {problema.estado_inicial: 0}
    
    while not frontera.empty():
        # Extraer el elemento con menor costo acumulado
        costo_acumulado, estado, camino = frontera.get()
        
        # Verificar si es estado meta
        if problema.es_meta(estado):
            return camino, costo_acumulado
        
        # Si encontramos un camino mejor a este estado, lo ignoramos
        if costo_acumulado > costos_minimos.get(estado, float('inf')):
            continue
        
        # Expandir el estado y añadir sucesores a la frontera
        for accion, costo_accion in problema.acciones_aplicables(estado):
            nuevo_estado, costo_transicion = problema.resultado(estado, accion)
            nuevo_costo = costo_acumulado + costo_accion
            nuevo_camino = camino + [accion]
            
            # Si encontramos un camino mejor al nuevo estado
            if nuevo_costo < costos_minimos.get(nuevo_estado, float('inf')):
                costos_minimos[nuevo_estado] = nuevo_costo
                frontera.put((nuevo_costo, nuevo_estado, nuevo_camino))
    
    # Si se agotó la frontera sin encontrar solución
    return None

# Ejemplo: Mundo del Robot en una cuadrícula 3x3 con costos variables
def crear_problema_robot_con_costos() -> ProblemaPlanificacionBusqueda:
    """
    Crea un problema de planificación para un robot en una cuadrícula 3x3 con costos variables
    
    Estados: A, B, C, D, E, F, G, H, I (de izquierda a derecha, arriba a abajo)
    Acciones: mover_arriba, mover_abajo, mover_izq, mover_der con diferentes costos
    """
    acciones = {
        'A': [('mover_der', 'B', 1.5), ('mover_abajo', 'D', 1.0)],
        'B': [('mover_izq', 'A', 1.5), ('mover_der', 'C', 1.0), ('mover_abajo', 'E', 0.8)],
        'C': [('mover_izq', 'B', 1.0), ('mover_abajo', 'F', 1.2)],
        'D': [('mover_arriba', 'A', 1.0), ('mover_der', 'E', 0.5), ('mover_abajo', 'G', 1.5)],
        'E': [('mover_arriba', 'B', 0.8), ('mover_izq', 'D', 0.5), ('mover_der', 'F', 0.5), ('mover_abajo', 'H', 0.5)],
        'F': [('mover_arriba', 'C', 1.2), ('mover_izq', 'E', 0.5), ('mover_abajo', 'I', 1.0)],
        'G': [('mover_arriba', 'D', 1.5), ('mover_der', 'H', 1.0)],
        'H': [('mover_arriba', 'E', 0.5), ('mover_izq', 'G', 1.0), ('mover_der', 'I', 0.8)],
        'I': [('mover_arriba', 'F', 1.0), ('mover_izq', 'H', 0.8)]
    }
    
    estado_inicial = 'A'
    estados_meta = {'I'}  # Queremos llegar a la posición I
    
    return ProblemaPlanificacionBusqueda(estado_inicial, estados_meta, acciones)

if __name__ == "__main__":
    # Crear y resolver el problema
    problema_robot = crear_problema_robot_con_costos()
    resultado = busqueda_costo_uniforme(problema_robot)
    
    # Mostrar resultados
    print("=== Búsqueda de Costo Uniforme para Planificación ===")
    print(f"Estado inicial: {problema_robot.estado_inicial}")
    print(f"Estado(s) meta: {problema_robot.estados_meta}")
    
    if resultado:
        plan, costo_total = resultado
        print("\nPlan encontrado:")
        for i, accion in enumerate(plan, 1):
            print(f"{i}. {accion}")
        print(f"\nCosto total del plan: {costo_total}")
        
        # Mostrar camino completo con estados intermedios
        print("\nCamino completo:")
        estado_actual = problema_robot.estado_inicial
        print(f"Estado: {estado_actual}")
        for accion in plan:
            estado_actual, _ = problema_robot.resultado(estado_actual, accion)
            print(f"Acción: {accion} → Estado: {estado_actual}")
    else:
        print("\nNo se encontró solución")