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

def busqueda_bidireccional(problema: ProblemaPlanificacionBusqueda) -> Optional[List[Accion]]:
    """
    Implementación de búsqueda bidireccional para planificación
    
    Args:
        problema: Problema de planificación como búsqueda
        
    Returns:
        Lista de acciones que llevan del estado inicial a un estado meta, o None si no hay solución
    """
    # Verificación rápida si el estado inicial es meta
    if problema.es_meta(problema.estado_inicial):
        return []
    
    # Estructuras para la búsqueda hacia adelante (desde inicial)
    frontera_adelante = deque()
    frontera_adelante.append((problema.estado_inicial, []))
    visitados_adelante = {problema.estado_inicial: []}
    
    # Estructuras para la búsqueda hacia atrás (desde meta)
    frontera_atras = deque()
    # Para búsqueda hacia atrás, necesitamos invertir las acciones
    acciones_invertidas = invertir_acciones(problema.acciones)
    for estado_meta in problema.estados_meta:
        frontera_atras.append((estado_meta, []))
        visitados_atras = {estado_meta: []}
    
    while frontera_adelante and frontera_atras:
        # Paso hacia adelante
        estado_actual_adelante, camino_adelante = frontera_adelante.popleft()
        
        # Verificar intersección
        if estado_actual_adelante in visitados_atras:
            camino_atras = visitados_atras[estado_actual_adelante]
            return camino_adelante + invertir_camino(camino_atras)
        
        # Expandir hacia adelante
        for accion in problema.acciones_aplicables(estado_actual_adelante):
            nuevo_estado = problema.resultado(estado_actual_adelante, accion)
            if nuevo_estado not in visitados_adelante:
                visitados_adelante[nuevo_estado] = camino_adelante + [accion]
                frontera_adelante.append((nuevo_estado, camino_adelante + [accion]))
        
        # Paso hacia atrás
        estado_actual_atras, camino_atras = frontera_atras.popleft()
        
        # Verificar intersección
        if estado_actual_atras in visitados_adelante:
            camino_adelante = visitados_adelante[estado_actual_atras]
            return camino_adelante + invertir_camino(camino_atras)
        
        # Expandir hacia atrás (usando acciones invertidas)
        for accion in acciones_invertidas.get(estado_actual_atras, []):
            nuevo_estado = problema.resultado(estado_actual_atras, accion)
            if nuevo_estado not in visitados_atras:
                visitados_atras[nuevo_estado] = camino_atras + [accion]
                frontera_atras.append((nuevo_estado, camino_atras + [accion]))
    
    return None

def invertir_acciones(acciones: ProblemaBusqueda) -> ProblemaBusqueda:
    """Invierte las direcciones de las acciones para búsqueda hacia atrás"""
    acciones_invertidas = {}
    for estado, transiciones in acciones.items():
        for accion, estado_siguiente in transiciones:
            if estado_siguiente not in acciones_invertidas:
                acciones_invertidas[estado_siguiente] = []
            acciones_invertidas[estado_siguiente].append((accion, estado))
    return acciones_invertidas

def invertir_camino(camino: List[Accion]) -> List[Accion]:
    """Invierte el orden de un camino (para búsqueda hacia atrás)"""
    return list(reversed(camino))

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
    plan = busqueda_bidireccional(problema_robot)
    
    # Mostrar resultados
    print("=== Búsqueda Bidireccional para Planificación ===")
    print(f"Estado inicial: {problema_robot.estado_inicial}")
    print(f"Estado(s) meta: {problema_robot.estados_meta}")
    
    if plan:
        print("\nPlan encontrado:")
        for i, accion in enumerate(plan, 1):
            print(f"{i}. {accion}")
        print(f"\nTotal de acciones: {len(plan)}")
        
        # Mostrar camino completo con estados intermedios
        print("\nCamino completo:")
        estado_actual = problema_robot.estado_inicial
        print(f"Estado: {estado_actual}")
        for accion in plan:
            estado_actual = problema_robot.resultado(estado_actual, accion)
            print(f"Acción: {accion} → Estado: {estado_actual}")
    else:
        print("\nNo se encontró solución")