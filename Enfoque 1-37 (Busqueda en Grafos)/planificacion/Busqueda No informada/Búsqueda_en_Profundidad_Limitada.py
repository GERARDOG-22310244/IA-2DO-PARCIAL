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

def busqueda_profundidad_limitada(
    problema: ProblemaPlanificacionBusqueda, 
    limite_profundidad: int = 5,
    estrategia: str = 'recursiva'
) -> Optional[List[Accion]]:
    """
    Implementación de búsqueda en profundidad limitada para planificación
    
    Args:
        problema: Problema de planificación como búsqueda
        limite_profundidad: Máxima profundidad de búsqueda
        estrategia: 'recursiva' o 'iterativa'
        
    Returns:
        Lista de acciones que llevan del estado inicial a un estado meta, o None si no hay solución
    """
    if estrategia == 'recursiva':
        def dls_recursiva(estado: Estado, camino: List[Accion], profundidad: int, visitados: Set[Estado]) -> Optional[List[Accion]]:
            if problema.es_meta(estado):
                return camino
            
            if profundidad >= limite_profundidad:
                return None
            
            visitados.add(estado)
            
            for accion in problema.acciones_aplicables(estado):
                nuevo_estado = problema.resultado(estado, accion)
                if nuevo_estado not in visitados:
                    resultado = dls_recursiva(nuevo_estado, camino + [accion], profundidad + 1, visitados.copy())
                    if resultado is not None:
                        return resultado
            return None
        
        return dls_recursiva(problema.estado_inicial, [], 0, set())
    
    else:  # Versión iterativa
        frontera = [(problema.estado_inicial, [], 0)]  # (estado, camino, profundidad)
        visitados = set()
        
        while frontera:
            estado, camino, profundidad = frontera.pop()
            
            if problema.es_meta(estado):
                return camino
                
            if profundidad >= limite_profundidad:
                continue
                
            if estado not in visitados:
                visitados.add(estado)
                
                for accion in reversed(problema.acciones_aplicables(estado)):  # reversed para mantener orden
                    nuevo_estado = problema.resultado(estado, accion)
                    frontera.append((nuevo_estado, camino + [accion], profundidad + 1))
        
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
    # Crear problema
    problema_robot = crear_problema_robot()
    
    print("=== Búsqueda en Profundidad Limitada (DLS) para Planificación ===")
    print(f"Estado inicial: {problema_robot.estado_inicial}")
    print(f"Estado(s) meta: {problema_robot.estados_meta}")
    
    # Pruebas con diferentes límites de profundidad
    for limite in [2, 4, 6, 8]:
        print(f"\nLímite de profundidad: {limite}")
        
        # Versión recursiva
        print("\nVersión recursiva:")
        plan_rec = busqueda_profundidad_limitada(problema_robot, limite, 'recursiva')
        if plan_rec:
            print("Plan encontrado:")
            for i, accion in enumerate(plan_rec, 1):
                print(f"{i}. {accion}")
            print(f"Total de acciones: {len(plan_rec)}")
        else:
            print("No se encontró solución")
        
        # Versión iterativa
        print("\nVersión iterativa:")
        plan_it = busqueda_profundidad_limitada(problema_robot, limite, 'iterativa')
        if plan_it:
            print("Plan encontrado:")
            for i, accion in enumerate(plan_it, 1):
                print(f"{i}. {accion}")
            print(f"Total de acciones: {len(plan_it)}")
        else:
            print("No se encontró solución")