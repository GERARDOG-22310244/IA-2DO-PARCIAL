from collections import defaultdict, deque
from typing import List, Dict, Set, Tuple, Optional
import random
import math

# Definición de tipos
Estado = str
Accion = str
ProblemaBusqueda = Dict[Estado, List[Tuple[Accion, Estado, float]]]  # Acción, Estado, Costo

class ProblemaPlanificacionOnline:
    def __init__(self, estado_inicial: Estado, estados_meta: Set[Estado], acciones: ProblemaBusqueda):
        """
        Inicializa un problema de planificación con búsqueda online
        
        Args:
            estado_inicial: Estado inicial del problema
            estados_meta: Conjunto de estados meta
            acciones: Diccionario de acciones por estado con costos
        """
        self.estado_inicial = estado_inicial
        self.estados_meta = estados_meta
        self.acciones = acciones
        self.estado_actual = estado_inicial
        self.camino = []
        self.costo_acumulado = 0.0
    
    def es_meta(self, estado: Estado) -> bool:
        """Verifica si un estado es estado meta"""
        return estado in self.estados_meta
    
    def acciones_aplicables(self, estado: Estado) -> List[Tuple[Accion, Estado, float]]:
        """Devuelve las acciones aplicables en un estado con sus resultados y costos"""
        return self.acciones.get(estado, [])
    
    def ejecutar_accion(self, accion: Accion) -> Tuple[Estado, float]:
        """Ejecuta una acción y actualiza el estado actual"""
        for a, s, c in self.acciones.get(self.estado_actual, []):
            if a == accion:
                self.camino.append(accion)
                self.costo_acumulado += c
                self.estado_actual = s
                return s, c
        return self.estado_actual, 0.0  # Si la acción no es aplicable
    
    def retroceder(self, pasos: int = 1) -> Estado:
        """Retrocede en el camino (simulando replanificación)"""
        if len(self.camino) >= pasos:
            # Reconstruir el estado anterior (simplificado)
            self.camino = self.camino[:-pasos]
            self.costo_acumulado -= sum(c for _, _, c in self.acciones.get(self.estado_actual, []))
            self.estado_actual = self.reconstruir_estado(self.estado_inicial, self.camino)
        return self.estado_actual
    
    def reconstruir_estado(self, estado_inicial: Estado, camino: List[Accion]) -> Estado:
        """Reconstruye el estado a partir del camino"""
        estado = estado_inicial
        for accion in camino:
            for a, s, _ in self.acciones.get(estado, []):
                if a == accion:
                    estado = s
                    break
        return estado

class BusquedaOnline:
    def __init__(self, problema: ProblemaPlanificacionOnline, horizonte: int = 3):
        """
        Inicializa el algoritmo de búsqueda online
        
        Args:
            problema: Problema de planificación online
            horizonte: Profundidad de búsqueda para la planificación local
        """
        self.problema = problema
        self.horizonte = horizonte
        self.plan_actual = []
    
    def planificar(self) -> Optional[List[Accion]]:
        """Realiza planificación local dentro del horizonte"""
        frontera = deque()
        frontera.append((self.problema.estado_actual, [], 0.0))  # (estado, camino, costo)
        
        mejor_camino = None
        mejor_costo = math.inf
        
        while frontera:
            estado, camino, costo = frontera.popleft()
            
            if self.problema.es_meta(estado):
                if costo < mejor_costo:
                    mejor_camino = camino
                    mejor_costo = costo
                continue
            
            if len(camino) >= self.horizonte:
                continue
            
            for accion, estado_sig, costo_accion in self.problema.acciones_aplicables(estado):
                frontera.append((estado_sig, camino + [accion], costo + costo_accion))
        
        self.plan_actual = mejor_camino if mejor_camino else []
        return self.plan_actual.copy()
    
    def ejecutar_paso(self) -> Tuple[bool, Optional[Accion]]:
        """Ejecuta un paso del plan actual"""
        if not self.plan_actual:
            self.planificar()
            if not self.plan_actual:
                return True, None  # Fin (no hay solución)
        
        accion = self.plan_actual.pop(0)
        estado_anterior = self.problema.estado_actual
        nuevo_estado, costo = self.problema.ejecutar_accion(accion)
        
        # Verificar si el resultado fue el esperado
        esperado = next((s for a, s, c in self.problema.acciones.get(estado_anterior, []) if a == accion), None)
        if nuevo_estado != esperado:
            # Replanificar debido a discrepancia
            self.problema.retroceder()
            self.plan_actual = []
            return False, None
        
        return self.problema.es_meta(nuevo_estado), accion

# Ejemplo: Mundo del Robot con incertidumbre
def crear_problema_robot_online() -> ProblemaPlanificacionOnline:
    """
    Crea un problema de planificación online para un robot en un entorno con incertidumbre
    
    Estados: A, B, C, D, E, F, G, H, I (cuadrícula 3x3)
    Acciones: mover con posibles fallos y costos variables
    """
    acciones = {
        'A': [('mover_der', 'B', 1.0), ('mover_abajo', 'D', 1.2)],
        'B': [('mover_izq', 'A', 1.0), ('mover_der', 'C', 1.0), ('mover_abajo', 'E', 0.8)],
        'C': [('mover_izq', 'B', 1.0), ('mover_abajo', 'F', 1.2)],
        'D': [('mover_arriba', 'A', 1.2), ('mover_der', 'E', 0.5), ('mover_abajo', 'G', 1.5)],
        'E': [('mover_arriba', 'B', 0.8), ('mover_izq', 'D', 0.5), ('mover_der', 'F', 0.5), ('mover_abajo', 'H', 0.5)],
        'F': [('mover_arriba', 'C', 1.2), ('mover_izq', 'E', 0.5), ('mover_abajo', 'I', 1.0)],
        'G': [('mover_arriba', 'D', 1.5), ('mover_der', 'H', 1.0)],
        'H': [('mover_arriba', 'E', 0.5), ('mover_izq', 'G', 1.0), ('mover_der', 'I', 0.8)],
        'I': [('mover_arriba', 'F', 1.0), ('mover_izq', 'H', 0.8)]
    }
    
    # Añadir incertidumbre (10% de probabilidad de fallo)
    for estado in list(acciones.keys()):
        for i, (accion, estado_sig, costo) in enumerate(acciones[estado]):
            if random.random() < 0.1:  # 10% de fallo
                estados_posibles = [s for s in acciones.keys() if s != estado_sig]
                if estados_posibles:
                    estado_fallo = random.choice(estados_posibles)
                    acciones[estado][i] = (accion, estado_fallo, costo * 1.5)
    
    estado_inicial = 'A'
    estados_meta = {'I'}
    
    return ProblemaPlanificacionOnline(estado_inicial, estados_meta, acciones)

def simulacion_online():
    """Simula la ejecución de búsqueda online"""
    problema = crear_problema_robot_online()
    buscador = BusquedaOnline(problema, horizonte=4)
    
    print("=== Simulación de Búsqueda Online ===")
    print(f"Estado inicial: {problema.estado_actual}")
    print(f"Meta: {problema.estados_meta}")
    print(f"Horizonte de planificación: {buscador.horizonte}")
    
    paso = 1
    terminado = False
    while not terminado:
        terminado, accion = buscador.ejecutar_paso()
        
        if accion is None and not terminado:
            print(f"\nPaso {paso}: Replanificando...")
            buscador.planificar()
            if not buscador.plan_actual:
                print("¡No se encontró solución!")
                break
            continue
        
        if accion:
            print(f"\nPaso {paso}:")
            print(f"Acción ejecutada: {accion}")
            print(f"Estado actual: {problema.estado_actual}")
            print(f"Costo acumulado: {problema.costo_acumulado:.2f}")
            print(f"Plan actual: {buscador.plan_actual}")
            paso += 1
    
    if terminado and problema.es_meta(problema.estado_actual):
        print("\n¡Meta alcanzada!")
        print(f"Camino final: {problema.camino}")
        print(f"Costo total: {problema.costo_acumulado:.2f}")
    else:
        print("\nNo se pudo alcanzar la meta")

if __name__ == "__main__":
    # Ejecutar simulación
    simulacion_online()