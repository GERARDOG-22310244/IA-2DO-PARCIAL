import numpy as np
import matplotlib.pyplot as plt
from collections import defaultdict
from sympy import symbols, Eq, Function
from sympy.logic.boolalg import And, Or, Not
import networkx as nx
import skfuzzy as fuzz
from skfuzzy.control import ControlSystem, Rule, Antecedent, Consequent

## ----------------------------
## 1. Lógica Modal
## ----------------------------

class ModeloKripke:
    def __init__(self):
        self.mundos = set()
        self.relacion = defaultdict(set)
        self.valuaciones = {}
    
    def agregar_mundo(self, mundo, valuacion=None):
        self.mundos.add(mundo)
        if valuacion:
            self.valuaciones[mundo] = valuacion
    
    def agregar_relacion(self, mundo1, mundo2):
        self.relacion[mundo1].add(mundo2)
    
    def evaluar(self, formula, mundo):
        """Evalúa una fórmula modal en un mundo"""
        if isinstance(formula, str):
            return formula in self.valuaciones.get(mundo, set())
        elif isinstance(formula, Not):
            return not self.evaluar(formula.args[0], mundo)
        elif isinstance(formula, And):
            return self.evaluar(formula.args[0], mundo) and self.evaluar(formula.args[1], mundo)
        elif isinstance(formula, Or):
            return self.evaluar(formula.args[0], mundo) or self.evaluar(formula.args[1], mundo)
        elif formula.func.__name__ == 'Necesario':
            # □φ es verdadero si φ es verdadero en todos los mundos accesibles
            return all(self.evaluar(formula.args[0], m) for m in self.relacion[mundo])
        elif formula.func.__name__ == 'Posible':
            # ◇φ es verdadero si φ es verdadero en algún mundo accesible
            return any(self.evaluar(formula.args[0], m) for m in self.relacion[mundo])
        return False

    def visualizar(self):
        """Visualiza el modelo de Kripke"""
        G = nx.DiGraph()
        for mundo in self.mundos:
            etiqueta = f"{mundo}\n{self.valuaciones.get(mundo, set())}"
            G.add_node(mundo, label=etiqueta)
        
        for origen, destinos in self.relacion.items():
            for destino in destinos:
                G.add_edge(origen, destino)
        
        pos = nx.spring_layout(G)
        labels = nx.get_node_attributes(G, 'label')
        nx.draw(G, pos, labels=labels, with_labels=True, node_size=2000, node_color='skyblue')
        plt.title("Modelo de Kripke")
        plt.show()

# Ejemplo de lógica modal
print("\nLógica Modal - Modelo de Kripke:")
kripke = ModeloKripke()
kripke.agregar_mundo('w1', {'p'})
kripke.agregar_mundo('w2', {'q'})
kripke.agregar_mundo('w3', {'p', 'q'})
kripke.agregar_relacion('w1', 'w2')
kripke.agregar_relacion('w1', 'w3')
kripke.agregar_relacion('w2', 'w3')

# Definir operadores modales
def Necesario(phi):
    return type('Necesario', (), {'args': (phi,), 'func': Necesario})

def Posible(phi):
    return type('Posible', (), {'args': (phi,), 'func': Posible})

# Evaluar fórmulas
formula1 = Necesario('q')
formula2 = Posible(And('p', 'q'))
print(f"□q en w1: {kripke.evaluar(formula1, 'w1')}")
print(f"◇(p∧q) en w1: {kripke.evaluar(formula2, 'w1')}")

kripke.visualizar()

## ----------------------------
## 2. Lógica Temporal (LTL)
## ----------------------------

class LTLModelChecker:
    def __init__(self, estados, transiciones, etiquetas):
        self.estados = estados
        self.transiciones = transiciones
        self.etiquetas = etiquetas
    
    def verificar(self, formula, estado_actual, camino=None):
        """Verifica una fórmula LTL"""
        if camino is None:
            camino = []
        
        if estado_actual in camino:
            return False  # Evitar ciclos infinitos
        
        if formula[0] == 'p':  # Proposición atómica
            return formula in self.etiquetas.get(estado_actual, set())
        elif formula[0] == '¬':
            return not self.verificar(formula[1], estado_actual, camino)
        elif formula[0] == '∧':
            return self.verificar(formula[1], estado_actual, camino) and self.verificar(formula[2], estado_actual, camino)
        elif formula[0] == 'X':  # Next
            return all(self.verificar(formula[1], s, camino + [estado_actual]) 
                   for s in self.transiciones.get(estado_actual, []))
        elif formula[0] == 'F':  # Future (Eventually)
            if self.verificar(formula[1], estado_actual, camino):
                return True
            return any(self.verificar(formula, s, camino + [estado_actual])
                   for s in self.transiciones.get(estado_actual, []))
        elif formula[0] == 'G':  # Globally (Always)
            if not self.verificar(formula[1], estado_actual, camino):
                return False
            return all(self.verificar(formula, s, camino + [estado_actual])
                   for s in self.transiciones.get(estado_actual, []))
        elif formula[0] == 'U':  # Until
            if self.verificar(formula[2], estado_actual, camino):
                return True
            if not self.verificar(formula[1], estado_actual, camino):
                return False
            return any(self.verificar(formula, s, camino + [estado_actual])
                   for s in self.transiciones.get(estado_actual, []))
        return False

# Ejemplo de lógica temporal
print("\nLógica Temporal (LTL):")
estados = ['s0', 's1', 's2']
transiciones = {'s0': ['s1'], 's1': ['s2'], 's2': ['s0']}
etiquetas = {'s0': {'p'}, 's1': {'q'}, 's2': {'p', 'q'}}

ltl = LTLModelChecker(estados, transiciones, etiquetas)

# Fórmulas LTL
formula_ltl1 = ('F', 'q')  # Eventualmente q
formula_ltl2 = ('G', ('¬', 'q'))  # Siempre no q
print(f"Fq en s0: {ltl.verificar(formula_ltl1, 's0')}")
print(f"G¬q en s0: {ltl.verificar(formula_ltl2, 's0')}")

## ----------------------------
## 3. Lógica Difusa
## ----------------------------

def sistema_difuso_temperatura():
    """Sistema de control difuso para temperatura"""
    # Variables de entrada y salida
    temperatura = Antecedent(np.arange(0, 41, 1), 'temperatura')
    potencia = Consequent(np.arange(0, 101, 1), 'potencia')
    
    # Funciones de membresía
    temperatura.automf(3, names=['fria', 'media', 'caliente'])
    potencia['baja'] = fuzz.trimf(potencia.universe, [0, 0, 50])
    potencia['media'] = fuzz.trimf(potencia.universe, [0, 50, 100])
    potencia['alta'] = fuzz.trimf(potencia.universe, [50, 100, 100])
    
    # Reglas difusas
    regla1 = Rule(temperatura['fria'], potencia['alta'])
    regla2 = Rule(temperatura['media'], potencia['media'])
    regla3 = Rule(temperatura['caliente'], potencia['baja'])
    
    # Sistema de control
    sistema_control = ControlSystem([regla1, regla2, regla3])
    sistema = ControlSystemSimulation(sistema_control)
    
    # Visualización
    temperatura.view()
    potencia.view()
    plt.show()
    
    # Ejemplo de cálculo
    sistema.input['temperatura'] = 15
    sistema.compute()
    print(f"\nLógica Difusa - Potencia para 15°C: {sistema.output['potencia']:.2f}%")
    potencia.view(sim=sistema)
    plt.show()

# Ejecutar sistema difuso
print("\nLógica Difusa - Sistema de Control de Temperatura:")
sistema_difuso_temperatura()