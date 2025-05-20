from collections import namedtuple, defaultdict
from itertools import product
from typing import List, Dict, Set, Optional

# 1. Representación del problema de planificación
Estado = frozenset  # Conjunto de proposiciones verdaderas
Accion = namedtuple('Accion', ['nombre', 'precondiciones', 'efectos_pos', 'efectos_neg'])

class ProblemaPlanificacion:
    def __init__(self, acciones: List[Accion], estado_inicial: Estado, metas: Estado):
        self.acciones = acciones
        self.estado_inicial = estado_inicial
        self.metas = metas
    
    def es_aplicable(self, accion: Accion, estado: Estado) -> bool:
        """Verifica si una acción es aplicable en un estado dado"""
        return accion.precondiciones.issubset(estado)
    
    def aplicar_accion(self, accion: Accion, estado: Estado) -> Estado:
        """Aplica una acción a un estado y devuelve el nuevo estado"""
        if not self.es_aplicable(accion, estado):
            return estado
        
        nuevo_estado = (estado - accion.efectos_neg) | accion.efectos_pos
        return nuevo_estado
    
    def es_estado_meta(self, estado: Estado) -> bool:
        """Verifica si un estado satisface las metas"""
        return self.metas.issubset(estado)

# 2. Búsqueda hacia adelante (forward search)
def planificacion_hacia_adelante(problema: ProblemaPlanificacion) -> Optional[List[str]]:
    """Implementa el algoritmo de búsqueda hacia adelante"""
    estado_actual = problema.estado_inicial
    plan = []
    
    # Búsqueda ingenua (para ejemplo didáctico)
    for _ in range(100):  # Límite de pasos
        if problema.es_estado_meta(estado_actual):
            return plan
        
        # Seleccionar una acción aplicable aleatoria
        acciones_aplicables = [a for a in problema.acciones 
                             if problema.es_aplicable(a, estado_actual)]
        
        if not acciones_aplicables:
            return None  # No se puede alcanzar la meta
        
        accion = acciones_aplicables[0]  # En una implementación real usaríamos una heurística
        plan.append(accion.nombre)
        estado_actual = problema.aplicar_accion(accion, estado_actual)
    
    return None

# 3. Planificación con orden parcial (STRIPS)
class PlanParcial:
    def __init__(self):
        self.acciones = []          # Lista de acciones en el plan
        self.ordenes = set()        # Restricciones de orden (A < B)
        self.enlaces = dict()       # Enlaces causales (p → A)
        self.literales = set()      # Literales necesarios
    
    def agregar_accion(self, accion: Accion, orden=None):
        """Añade una acción al plan con restricciones de orden"""
        self.acciones.append(accion)
        if orden:
            self.ordenes.add((orden, accion))
        return accion
    
    def agregar_enlace(self, literal, accion):
        """Establece que una acción provee un literal"""
        self.enlaces[literal] = accion
    
    def es_consistente(self) -> bool:
        """Verifica si el plan es consistente"""
        # Verificar que no haya ciclos en las restricciones de orden
        grafo = defaultdict(set)
        for a, b in self.ordenes:
            grafo[a].add(b)
        
        # Detección de ciclos con DFS
        visitados = set()
        for nodo in grafo:
            if nodo not in visitados:
                pila = [(nodo, False)]
                while pila:
                    actual, procesado = pila.pop()
                    if procesado:
                        continue
                    if actual in visitados:
                        return False  # Ciclo detectado
                    visitados.add(actual)
                    pila.append((actual, True))
                    pila.extend((vecino, False) for vecino in grafo[actual])
        return True

def strips(problema: ProblemaPlanificacion) -> Optional[PlanParcial]:
    """Algoritmo STRIPS simplificado"""
    plan = PlanParcial()
    accion_inicio = Accion('Inicio', frozenset(), problema.estado_inicial, frozenset())
    accion_fin = Accion('Fin', problema.metas, frozenset(), frozenset())
    
    plan.agregar_accion(accion_inicio)
    plan.agregar_accion(accion_fin)
    plan.agregar_enlace(None, accion_inicio)  # Enlace inicial
    
    # Para cada meta, encontrar una acción que la provea
    for meta in problema.metas:
        # Buscar acción que produzca esta meta
        accion_proveedora = None
        for accion in problema.acciones:
            if meta in accion.efectos_pos:
                accion_proveedora = accion
                break
        
        if not accion_proveedora:
            return None  # No se puede alcanzar la meta
        
        # Añadir acción al plan
        nueva_accion = plan.agregar_accion(accion_proveedora)
        plan.agregar_enlace(meta, nueva_accion)
        
        # Añadir restricción de orden: Inicio < nueva_accion < Fin
        plan.ordenes.add((accion_inicio, nueva_accion))
        plan.ordenes.add((nueva_accion, accion_fin))
        
        # Resolver precondiciones recursivamente
        for precond in accion_proveedora.precondiciones:
            if precond not in problema.estado_inicial:
                subplan = strips(ProblemaPlanificacion(
                    problema.acciones, 
                    problema.estado_inicial, 
                    frozenset([precond])
                ))
                if not subplan:
                    return None
                # Combinar subplanes (simplificado)
    
    if plan.es_consistente():
        return plan
    return None

# 4. Ejemplo: Mundo del robot
def ejemplo_mundo_robot():
    # Definir acciones
    acciones = [
        Accion('Mover(A,B)', 
               frozenset({'En(A)', 'Libre(B)'}), 
               frozenset({'En(B)'}), 
               frozenset({'En(A)', 'Libre(B)'})),
        Accion('Mover(B,A)', 
               frozenset({'En(B)', 'Libre(A)'}), 
               frozenset({'En(A)'}), 
               frozenset({'En(B)', 'Libre(A)'})),
        Accion('Cargar(C,A)', 
               frozenset({'En(A)', 'Cerca(C)'}), 
               frozenset({'Cargado(C)'}), 
               frozenset({'Cerca(C)'})),
        Accion('Descargar(C,B)', 
               frozenset({'En(B)', 'Cargado(C)'}), 
               frozenset({'Cerca(C)', 'Libre(B)'}), 
               frozenset({'Cargado(C)'}))
    ]
    
    # Definir problema
    estado_inicial = frozenset({'En(A)', 'Libre(B)', 'Cerca(C)'})
    metas = frozenset({'En(B)', 'Cerca(C)'})
    
    problema = ProblemaPlanificacion(acciones, estado_inicial, metas)
    
    # Resolver con búsqueda hacia adelante
    print("\nPlanificación hacia adelante:")
    plan_adelante = planificacion_hacia_adelante(problema)
    print("Plan encontrado:", plan_adelante)
    
    # Resolver con STRIPS (simplificado)
    print("\nPlanificación STRIPS (simplificada):")
    plan_strips = strips(problema)
    if plan_strips:
        print("Acciones en plan:", [a.nombre for a in plan_strips.acciones if a.nombre not in ['Inicio', 'Fin']])
        print("Restricciones de orden:", plan_strips.ordenes)
    else:
        print("No se encontró plan")

# 5. Planificación con GraphPlan
class GraphPlan:
    def __init__(self, problema: ProblemaPlanificacion):
        self.problema = problema
        self.niveles = []  # Lista de niveles (estados y acciones)
    
    def expandir(self):
        """Expande el grafo de planificación un nivel más"""
        if not self.niveles:
            # Primer nivel: estado inicial
            self.niveles.append({'estado': self.problema.estado_inicial, 'acciones': set()})
            return
        
        ultimo_nivel = self.niveles[-1]
        estado_actual = ultimo_nivel['estado']
        
        # Encontrar todas las acciones aplicables
        acciones_aplicables = set()
        for accion in self.problema.acciones:
            if self.problema.es_aplicable(accion, estado_actual):
                acciones_aplicables.add(accion)
        
        # Calcular nuevo estado
        nuevo_estado = estado_actual.copy()
        for accion in acciones_aplicables:
            nuevo_estado = (nuevo_estado - accion.efectos_neg) | accion.efectos_pos
        
        # Añadir nuevo nivel
        self.niveles.append({
            'estado': nuevo_estado,
            'acciones': acciones_aplicables
        })
    
    def buscar_plan(self) -> Optional[List[str]]:
        """Busca un plan en el grafo de planificación"""
        # Implementación simplificada
        for nivel in self.niveles:
            if self.problema.es_estado_meta(nivel['estado']):
                # Reconstruir plan (versión simplificada)
                plan = []
                for n in reversed(self.niveles):
                    if n['acciones']:
                        plan.append(next(iter(n['acciones'])).nombre)
                return list(reversed(plan))
        return None

def ejemplo_graphplan():
    # Definir acciones y problema (mismo ejemplo que antes)
    acciones = [
        Accion('Mover(A,B)', 
               frozenset({'En(A)', 'Libre(B)'}), 
               frozenset({'En(B)'}), 
               frozenset({'En(A)', 'Libre(B)'})),
        Accion('Mover(B,A)', 
               frozenset({'En(B)', 'Libre(A)'}), 
               frozenset({'En(A)'}), 
               frozenset({'En(B)', 'Libre(A)'})),
    ]
    
    estado_inicial = frozenset({'En(A)', 'Libre(B)'})
    metas = frozenset({'En(B)'})
    
    problema = ProblemaPlanificacion(acciones, estado_inicial, metas)
    
    # Crear y expandir GraphPlan
    gp = GraphPlan(problema)
    for _ in range(3):  # Expandir 3 niveles
        gp.expandir()
    
    # Buscar plan
    print("\nPlanificación con GraphPlan:")
    plan = gp.buscar_plan()
    print("Plan encontrado:", plan)

if __name__ == "__main__":
    print("=== Ejemplos de Planificación Automatizada ===")
    ejemplo_mundo_robot()
    ejemplo_graphplan()