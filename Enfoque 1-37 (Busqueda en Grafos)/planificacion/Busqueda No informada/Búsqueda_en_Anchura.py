from collections import deque
from typing import List, Dict, Set, Tuple, Optional

# Definición de tipos
Estado = str
Accion = str
ProblemaBusqueda = Dict[Estado, List[Tuple[Accion, Estado]]]

class ProblemaPlanificacionBusqueda:
    def __init__(self, estado_inicial: Estado, estados_meta: Set[Estado], acciones: ProblemaBusqueda):
        """
        Inicializa un problema de planificación como búsqueda
        
        Args:
            estado_inicial: Estado inicial del problema
            estados_meta: Conjunto de estados meta
            acciones: Diccionario de acciones por estado
        """
        self.estado_inicial = estado_inicial
        self.estados_meta = estados_meta
        self.acciones = acciones
    
    def es_meta(self, estado: Estado) -> bool:
        """Verifica si un estado es estado meta"""
        return estado in self.estados_meta
    
    def acciones_aplicables(self, estado: Estado) -> List[Accion]:
        """Devuelve las acciones aplicables en un estado"""
        return [accion for accion, _ in self.acciones.get(estado, [])]
    
    def resultado(self, estado: Estado, accion: Accion) -> Estado:
        """Aplica una acción a un estado y devuelve el nuevo estado"""
        for a, s in self.acciones.get(estado, []):
            if a == accion:
                return s
        return estado  # Si la acción no es aplicable, devuelve el mismo estado

def busqueda_anchura(problema: ProblemaPlanificacionBusqueda) -> Optional[List[Accion]]:
    """
    Implementación de búsqueda en anchura para planificación
    
    Args:
        problema: Problema de planificación como búsqueda
        
    Returns:
        Lista de acciones que llevan del estado inicial a un estado meta, o None si no hay solución
    """
    # Frontera: cola FIFO de tuplas (estado, camino)
    frontera = deque()
    frontera.append((problema.estado_inicial, []))
    
    # Conjunto de estados explorados
    explorados = set()
    
    while frontera:
        # Extraer el primer elemento de la frontera
        estado, camino = frontera.popleft()
        
        # Verificar si es estado meta
        if problema.es_meta(estado):
            return camino
        
        # Si no ha sido explorado, procesarlo
        if estado not in explorados:
            explorados.add(estado)
            
            # Expandir el estado y añadir sucesores a la frontera
            for accion in problema.acciones_aplicables(estado):
                nuevo_estado = problema.resultado(estado, accion)
                nuevo_camino = camino + [accion]
                frontera.append((nuevo_estado, nuevo_camino))
    
    # Si se agotó la frontera sin encontrar solución
    return None

# Ejemplo: Mundo del Robot en una cuadrícula 3x3
def crear_problema_robot() -> ProblemaPlanificacionBusqueda:
    """
    Crea un problema de planificación para un robot en una cuadrícula 3x3
    
    Estados: A, B, C, D, E, F, G, H, I (de izquierda a derecha, arriba a abajo)
    Acciones: mover_arriba, mover_abajo, mover_izq, mover_der
    """
    acciones = {
        'A': [('mover_der', 'B'), ('mover_abajo', 'D')],
        'B': [('mover_izq', 'A'), ('mover_der', 'C'), ('mover_abajo', 'E')],
        'C': [('mover_izq', 'B'), ('mover_abajo', 'F')],
        'D': [('mover_arriba', 'A'), ('mover_der', 'E'), ('mover_abajo', 'G')],
        'E': [('mover_arriba', 'B'), ('mover_izq', 'D'), ('mover_der', 'F'), ('mover_abajo', 'H')],
        'F': [('mover_arriba', 'C'), ('mover_izq', 'E'), ('mover_abajo', 'I')],
        'G': [('mover_arriba', 'D'), ('mover_der', 'H')],
        'H': [('mover_arriba', 'E'), ('mover_izq', 'G'), ('mover_der', 'I')],
        'I': [('mover_arriba', 'F'), ('mover_izq', 'H')]
    }
    
    estado_inicial = 'A'
    estados_meta = {'I'}  # Queremos llegar a la posición I
    
    return ProblemaPlanificacionBusqueda(estado_inicial, estados_meta, acciones)

if __name__ == "__main__":
    # Crear y resolver el problema
    problema_robot = crear_problema_robot()
    plan = busqueda_anchura(problema_robot)
    
    # Mostrar resultados
    print("=== Búsqueda en Anchura para Planificación ===")
    print(f"Estado inicial: {problema_robot.estado_inicial}")
    print(f"Estado(s) meta: {problema_robot.estados_meta}")
    
    if plan:
        print("\nPlan encontrado:")
        for i, accion in enumerate(plan, 1):
            print(f"{i}. {accion}")
        print(f"\nTotal de acciones: {len(plan)}")
    else:
        print("\nNo se encontró solución")