from collections import defaultdict, namedtuple
from sympy import symbols, And, Or, Not, Implies, Equivalent
from sympy.logic.inference import satisfiable

# 1. Representación con Lógica Proposicional
class SistemaConocimientoProposicional:
    def __init__(self):
        self.base_conocimiento = []
    
    def agregar_hecho(self, hecho):
        """Agrega un hecho a la base de conocimiento"""
        self.base_conocimiento.append(hecho)
    
    def agregar_regla(self, antecedente, consecuente):
        """Agrega una regla (implicación)"""
        self.base_conocimiento.append(Implies(antecedente, consecuente))
    
    def consultar(self, query):
        """Verifica si una consulta es consecuencia lógica"""
        return not satisfiable(And(*self.base_conocimiento, Not(query)))

# Ejemplo de uso
print("=== Lógica Proposicional ===")
p, q, r = symbols('p q r')
sistema_prop = SistemaConocimientoProposicional()
sistema_prop.agregar_hecho(p)
sistema_prop.agregar_regla(p, q)
sistema_prop.agregar_regla(q, r)

print("¿r es verdad?:", sistema_prop.consultar(r))
print("¿¬p es verdad?:", sistema_prop.consultar(Not(p)))

# 2. Representación con Lógica de Primer Orden
class SistemaConocimientoPrimerOrden:
    def __init__(self):
        self.hechos = set()
        self.reglas = []
    
    def agregar_hecho(self, hecho):
        self.hechos.add(hecho)
    
    def agregar_regla(self, antecedente, consecuente):
        self.reglas.append((antecedente, consecuente))
    
    def encadenamiento_hacia_adelante(self):
        """Motor de inferencia con encadenamiento hacia adelante"""
        nuevos_hechos = True
        while nuevos_hechos:
            nuevos_hechos = False
            for antecedente, consecuente in self.reglas:
                if antecedente in self.hechos and consecuente not in self.hechos:
                    self.hechos.add(consecuente)
                    nuevos_hechos = True
    
    def consultar(self, query):
        """Consulta si un hecho está en la base de conocimiento"""
        self.encadenamiento_hacia_adelante()
        return query in self.hechos

# Ejemplo de uso
print("\n=== Lógica de Primer Orden ===")
Hecho = namedtuple('Hecho', ['predicado', 'argumentos'])
P = 'P'
Q = 'Q'
R = 'R'

sistema_fo = SistemaConocimientoPrimerOrden()
sistema_fo.agregar_hecho(Hecho(P, ['a']))
sistema_fo.agregar_regla(Hecho(P, ['x']), Hecho(Q, ['x']))
sistema_fo.agregar_regla(Hecho(Q, ['x']), Hecho(R, ['x']))

print("¿R(a) es verdad?:", sistema_fo.consultar(Hecho(R, ['a'])))
print("Hechos conocidos:", sistema_fo.hechos)

# 3. Representación con Redes Semánticas
class RedSemantica:
    def __init__(self):
        self.nodos = set()
        self.relaciones = defaultdict(list)
    
    def agregar_nodo(self, nodo, tipo=None):
        self.nodos.add((nodo, tipo))
    
    def agregar_relacion(self, origen, relacion, destino):
        self.relaciones[origen].append((relacion, destino))
    
    def consultar(self, origen, relacion=None, destino=None):
        """Consulta relaciones en la red"""
        resultados = []
        for rel, dest in self.relaciones.get(origen, []):
            if (relacion is None or rel == relacion) and (destino is None or dest == destino):
                resultados.append((rel, dest))
        return resultados

# Ejemplo de uso
print("\n=== Red Semántica ===")
red = RedSemantica()
red.agregar_nodo('Perro', 'Animal')
red.agregar_nodo('Mamífero', 'Clase')
red.agregar_relacion('Perro', 'es-un', 'Mamífero')
red.agregar_relacion('Perro', 'tiene', 'Pelaje')

print("Relaciones de 'Perro':", red.consultar('Perro'))
print("¿Perro es-un Mamífero?:", bool(red.consultar('Perro', 'es-un', 'Mamífero')))

# 4. Representación con Marcos y Scripts
class Script:
    def __init__(self, nombre):
        self.nombre = nombre
        self.roles = {}
        self.secuencia = []
    
    def agregar_rol(self, nombre, valor=None):
        self.roles[nombre] = valor
    
    def agregar_evento(self, evento, orden=None):
        if orden is None:
            self.secuencia.append(evento)
        else:
            self.secuencia.insert(orden, evento)
    
    def ejecutar(self, contexto):
        """Ejecuta el script con un contexto dado"""
        resultado = defaultdict(list)
        for evento in self.secuencia:
            if callable(evento):
                evento(contexto, resultado)
            else:
                resultado['eventos'].append(evento)
        return resultado

# Ejemplo de uso
print("\n=== Scripts ===")
def saludar(ctx, res):
    res['acciones'].append(f"{ctx['persona']} saluda al {ctx['receptor']}")

script_restaurante = Script("Restaurante")
script_restaurante.agregar_rol("persona")
script_restaurante.agregar_rol("receptor", "mesero")
script_restaurante.agregar_evento(saludar)
script_restaurante.agregar_evento("Pedir menú")

contexto = {'persona': 'Juan', 'receptor': 'mesero'}
print("Ejecución del script:", script_restaurante.ejecutar(contexto))

# 5. Representación con Ontologías (simplificado)
class Ontologia:
    def __init__(self):
        self.clases = set()
        self.instancias = defaultdict(set)
        self.propiedades = defaultdict(dict)
    
    def agregar_clase(self, clase):
        self.clases.add(clase)
    
    def agregar_instancia(self, instancia, clase):
        self.instancias[clase].add(instancia)
    
    def agregar_propiedad(self, instancia, propiedad, valor):
        self.propiedades[instancia][propiedad] = valor
    
    def consultar(self, instancia=None, clase=None, propiedad=None):
        """Consulta la ontología"""
        resultados = []
        if instancia:
            if propiedad:
                return self.propiedades.get(instancia, {}).get(propiedad)
            return [c for c, insts in self.instancias.items() if instancia in insts]
        elif clase:
            return self.instancias.get(clase, set())
        return resultados

# Ejemplo de uso
print("\n=== Ontología ===")
ontologia = Ontologia()
ontologia.agregar_clase('Animal')
ontologia.agregar_clase('Mamifero')
ontologia.agregar_instancia('Fido', 'Mamifero')
ontologia.agregar_propiedad('Fido', 'patas', 4)

print("Instancias de Mamifero:", ontologia.consultar(clase='Mamifero'))
print("Patas de Fido:", ontologia.consultar(instancia='Fido', propiedad='patas'))