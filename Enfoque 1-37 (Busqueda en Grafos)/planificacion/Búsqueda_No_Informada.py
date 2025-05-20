from collections import deque
import random
from typing import List, Dict, Set, Tuple, Optional

# Definición de tipos
Estado = str
Accion = str
ProblemaBusqueda = Dict[str, List[Tuple[Accion, Estado]]]

## ----------------------------
## 1. Implementación de Problema de Búsqueda
## ----------------------------

class ProblemaPlanificacionBusqueda:
    def __init__(self, estado_inicial: Estado, estados_meta: Set[Estado], acciones: ProblemaBusqueda):
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

## ----------------------------
## 2. Algoritmos de Búsqueda No Informada
## ----------------------------

def busqueda_anchura(problema: ProblemaPlanificacionBusqueda) -> Optional[List[Accion]]:
    """Implementación de búsqueda en anchura"""
    frontera = deque()
    frontera.append((problema.estado_inicial, []))  # (estado, camino)
    explorados = set()
    
    while frontera:
        estado, camino = frontera.popleft()
        
        if problema.es_meta(estado):
            return camino
        
        if estado not in explorados:
            explorados.add(estado)
            
            for accion in problema.acciones_aplicables(estado):
                nuevo_estado = problema.resultado(estado, accion)
                nuevo_camino = camino + [accion]
                frontera.append((nuevo_estado, nuevo_camino))
    
    return None  # No se encontró solución

def busqueda_profundidad(problema: ProblemaPlanificacionBusqueda, limite_profundidad: int = 10) -> Optional[List[Accion]]:
    """Implementación de búsqueda en profundidad con límite"""
    frontera = []
    frontera.append((problema.estado_inicial, [], 0))  # (estado, camino, profundidad)
    explorados = set()
    
    while frontera:
        estado, camino, profundidad = frontera.pop()
        
        if problema.es_meta(estado):
            return camino
        
        if estado not in explorados and profundidad < limite_profundidad:
            explorados.add(estado)
            
            for accion in reversed(problema.acciones_aplicables(estado)):  # reversed para mantener orden
                nuevo_estado = problema.resultado(estado, accion)
                nuevo_camino = camino + [accion]
                frontera.append((nuevo_estado, nuevo_camino, profundidad + 1))
    
    return None  # No se encontró solución

def busqueda_profundidad_iterativa(problema: ProblemaPlanificacionBusqueda, incremento: int = 1) -> Optional[List[Accion]]:
    """Implementación de búsqueda en profundidad iterativa"""
    limite = 0
    
    while True:
        resultado = busqueda_profundidad(problema, limite)
        if resultado is not None:
            return resultado
        limite += incremento
        
        # Prevención contra bucles infinitos (para grafos muy grandes)
        if limite > 100:  # Límite arbitrario grande
            return None

def busqueda_costo_uniforme(problema: ProblemaPlanificacionBusqueda, costos: Dict[Tuple[Estado, Accion], float]) -> Optional[List[Accion]]:
    """Implementación de búsqueda de costo uniforme"""
    frontera = []
    frontera.append((0, problema.estado_inicial, []))  # (costo_acumulado, estado, camino)
    explorados = set()
    
    while frontera:
        frontera.sort()  # Ordenar por costo acumulado
        costo, estado, camino = frontera.pop(0)
        
        if problema.es_meta(estado):
            return camino
        
        if estado not in explorados:
            explorados.add(estado)
            
            for accion in problema.acciones_aplicables(estado):
                nuevo_estado = problema.resultado(estado, accion)
                nuevo_costo = costo + costos.get((estado, accion), 1)  # Costo 1 por defecto
                nuevo_camino = camino + [accion]
                frontera.append((nuevo_costo, nuevo_estado, nuevo_camino))
    
    return None  # No se encontró solución

## ----------------------------
## 3. Ejemplo: Mundo del Robot
## ----------------------------

def crear_problema_robot() -> ProblemaPlanificacionBusqueda:
    """Crea un problema de planificación para un robot"""
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

def crear_costos_robot() -> Dict[Tuple[Estado, Accion], float]:
    """Crea un diccionario de costos para las acciones del robot"""
    return {
        ('A', 'mover_der'): 1.0,
        ('A', 'mover_abajo'): 1.2,
        ('B', 'mover_izq'): 1.0,
        ('B', 'mover_der'): 1.0,
        ('B', 'mover_abajo'): 1.3,
        ('C', 'mover_izq'): 1.0,
        ('C', 'mover_abajo'): 1.1,
        ('D', 'mover_arriba'): 1.2,
        ('D', 'mover_der'): 1.0,
        ('D', 'mover_abajo'): 1.4,
        ('E', 'mover_arriba'): 1.3,
        ('E', 'mover_izq'): 1.0,
        ('E', 'mover_der'): 1.0,
        ('E', 'mover_abajo'): 1.5,
        ('F', 'mover_arriba'): 1.1,
        ('F', 'mover_izq'): 1.0,
        ('F', 'mover_abajo'): 1.2,
        ('G', 'mover_arriba'): 1.4,
        ('G', 'mover_der'): 1.0,
        ('H', 'mover_arriba'): 1.5,
        ('H', 'mover_izq'): 1.0,
        ('H', 'mover_der'): 1.0,
        ('I', 'mover_arriba'): 1.2,
        ('I', 'mover_izq'): 1.0
    }

## ----------------------------
## 4. Pruebas y Comparación
## ----------------------------

if __name__ == "__main__":
    print("=== Problema del Robot ===")
    problema_robot = crear_problema_robot()
    costos_robot = crear_costos_robot()
    
    print("\nBúsqueda en Anchura:")
    plan_anchura = busqueda_anchura(problema_robot)
    print("Plan encontrado:", plan_anchura)
    print("Longitud del plan:", len(plan_anchura) if plan_anchura else 0)
    
    print("\nBúsqueda en Profundidad (límite 10):")
    plan_profundidad = busqueda_profundidad(problema_robot, 10)
    print("Plan encontrado:", plan_profundidad)
    print("Longitud del plan:", len(plan_profundidad) if plan_profundidad else 0)
    
    print("\nBúsqueda en Profundidad Iterativa:")
    plan_prof_iterativa = busqueda_profundidad_iterativa(problema_robot)
    print("Plan encontrado:", plan_prof_iterativa)
    print("Longitud del plan:", len(plan_prof_iterativa) if plan_prof_iterativa else 0)
    
    print("\nBúsqueda de Costo Uniforme:")
    plan_costo_uniforme = busqueda_costo_uniforme(problema_robot, costos_robot)
    print("Plan encontrado:", plan_costo_uniforme)
    print("Longitud del plan:", len(plan_costo_uniforme) if plan_costo_uniforme else 0)
    
    # Análisis comparativo
    print("\n=== Comparación de Algoritmos ===")
    print("Algoritmo\t\tLongitud\tCosto\t\tCompleto\tÓptimo")
    print("----------------------------------------------------------------")
    
    # Búsqueda en anchura
    print("Anchura\t\t\t", len(plan_anchura) if plan_anchura else "-", 
          "\t\t", sum(costos_robot.get((estado, accion), 1) 
                     for estado, accion in zip([problema_robot.estado_inicial] + plan_anchura[:-1], plan_anchura)) 
                     if plan_anchura else "-",
          "\t\tSí\t\tSí")
    
    # Búsqueda en profundidad
    print("Profundidad\t\t", len(plan_profundidad) if plan_profundidad else "-", 
          "\t\t", sum(costos_robot.get((estado, accion), 1) 
                     for estado, accion in zip([problema_robot.estado_inicial] + plan_profundidad[:-1], plan_profundidad)) 
                     if plan_profundidad else "-",
          "\t\tNo\t\tNo")
    
    # Búsqueda en profundidad iterativa
    print("Prof. Iterativa\t\t", len(plan_prof_iterativa) if plan_prof_iterativa else "-", 
          "\t\t", sum(costos_robot.get((estado, accion), 1) 
                     for estado, accion in zip([problema_robot.estado_inicial] + plan_prof_iterativa[:-1], plan_prof_iterativa)) 
                     if plan_prof_iterativa else "-",
          "\t\tSí\t\tSí")
    
    # Búsqueda de costo uniforme
    print("Costo Uniforme\t\t", len(plan_costo_uniforme) if plan_costo_uniforme else "-", 
          "\t\t", sum(costos_robot.get((estado, accion), 1) 
                     for estado, accion in zip([problema_robot.estado_inicial] + plan_costo_uniforme[:-1], plan_costo_uniforme)) 
                     if plan_costo_uniforme else "-",
          "\t\tSí\t\tSí")