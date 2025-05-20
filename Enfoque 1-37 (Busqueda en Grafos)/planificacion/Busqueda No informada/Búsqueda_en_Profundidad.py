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

def busqueda_profundidad(problema: ProblemaPlanificacionBusqueda, limite_profundidad: int = 10) -> Optional[List[Accion]]:
    """
    Implementación de búsqueda en profundidad con límite para planificación
    
    Args:
        problema: Problema de planificación como búsqueda
        limite_profundidad: Máxima profundidad de búsqueda
        
    Returns:
        Lista de acciones que llevan del estado inicial a un estado meta, o None si no hay solución
    """
    # Usamos recursión para implementar DFS (con límite de profundidad)
    def dfs(estado: Estado, camino: List[Accion], profundidad: int, visitados: Set[Estado]) -> Optional[List[Accion]]:
        # Verificar si es estado meta
        if problema.es_meta(estado):
            return camino
        
        # Verificar límite de profundidad
        if profundidad >= limite_profundidad:
            return None
        
        # Marcar como visitado
        visitados.add(estado)
        
        # Explorar acciones en orden
        for accion in problema.acciones_aplicables(estado):
            nuevo_estado = problema.resultado(estado, accion)
            
            # Evitar ciclos (no visitar estados ya explorados en este camino)
            if nuevo_estado not in visitados:
                resultado = dfs(nuevo_estado, camino + [accion], profundidad + 1, visitados.copy())
                if resultado is not None:
                    return resultado
        
        return None
    
    # Llamada inicial a la función recursiva
    return dfs(problema.estado_inicial, [], 0, set())

# Versión iterativa (sin recursión)
def busqueda_profundidad_iterativa(problema: ProblemaPlanificacionBusqueda) -> Optional[List[Accion]]:
    """
    Implementación de búsqueda en profundidad iterativa para planificación
    
    Args:
        problema: Problema de planificación como búsqueda
        
    Returns:
        Lista de acciones que llevan del estado inicial a un estado meta, o None si no hay solución
    """
    limite = 0
    while True:
        resultado = busqueda_profundidad(problema, limite)
        if resultado is not None:
            return resultado
        limite += 1
        
        # Prevención contra bucles infinitos (para grafos muy grandes)
        if limite > 100:  # Límite arbitrario grande
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
    
    print("=== Búsqueda en Profundidad (DFS) para Planificación ===")
    print(f"Estado inicial: {problema_robot.estado_inicial}")
    print(f"Estado(s) meta: {problema_robot.estados_meta}")
    
    # Prueba con DFS estándar (límite 10)
    print("\nBúsqueda en Profundidad (límite 10):")
    plan_dfs = busqueda_profundidad(problema_robot, 10)
    if plan_dfs:
        print("Plan encontrado:")
        for i, accion in enumerate(plan_dfs, 1):
            print(f"{i}. {accion}")
        print(f"\nTotal de acciones: {len(plan_dfs)}")
    else:
        print("No se encontró solución con límite de profundidad 10")
    
    # Prueba con DFS iterativo
    print("\nBúsqueda en Profundidad Iterativa:")
    plan_idfs = busqueda_profundidad_iterativa(problema_robot)
    if plan_idfs:
        print("Plan encontrado:")
        for i, accion in enumerate(plan_idfs, 1):
            print(f"{i}. {accion}")
        print(f"\nTotal de acciones: {len(plan_idfs)}")
    else:
        print("No se encontró solución")