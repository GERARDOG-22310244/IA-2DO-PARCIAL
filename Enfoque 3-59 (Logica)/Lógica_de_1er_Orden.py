from sympy import symbols, Function, ForAll, Exists, Implies, And, Or, Not
from sympy.logic.inference import satisfiable

# 1. Definición de símbolos
x, y, z = symbols('x y z')  # Variables
P = Function('P')  # Predicado unario
Q = Function('Q')  # Predicado binario
a, b, c = symbols('a b c')  # Constantes

# 2. Ejemplos de fórmulas de primer orden
formula1 = ForAll(x, P(x))  # ∀x P(x)
formula2 = Exists(y, Q(y, a))  # ∃y Q(y,a)
formula3 = Implies(ForAll(x, P(x)), Exists(y, P(y)))  # ∀x P(x) → ∃y P(y)
formula4 = ForAll(x, Exists(y, Q(x, y)))  # ∀x∃y Q(x,y)

print("Fórmulas de Primer Orden:")
print(f"1. {formula1}")
print(f"2. {formula2}")
print(f"3. {formula3}")
print(f"4. {formula4}")

# 3. Skolemización (transformación a forma normal)
def skolemize(formula):
    """Convierte una fórmula a forma normal Skolem (simplificada)"""
    if isinstance(formula, ForAll):
        return skolemize(formula.function)
    elif isinstance(formula, Exists):
        # Reemplazar variable existencial con constante de Skolem
        return formula.function.subs(formula.variables[0], symbols(f's{formula.variables[0]}'))
    elif isinstance(formula, (And, Or)):
        return formula.func(*[skolemize(arg) for arg in formula.args])
    elif isinstance(formula, Not):
        return Not(skolemize(formula.args[0]))
    elif isinstance(formula, Implies):
        return Implies(skolemize(formula.args[0]), skolemize(formula.args[1]))
    return formula

print("\nSkolemización de fórmula 4:")
print(skolemize(formula4))

# 4. Unificación (versión simplificada)
def unificar(term1, term2, sust=None):
    """Algoritmo de unificación para términos de primer orden"""
    if sust is None:
        sust = {}
    
    if term1 == term2:
        return sust
    elif isinstance(term1, str) and term1.islower():  # Variable
        return unificar_var(term1, term2, sust)
    elif isinstance(term2, str) and term2.islower():  # Variable
        return unificar_var(term2, term1, sust)
    elif isinstance(term1, Function) and isinstance(term2, Function):
        if term1.func != term2.func or len(term1.args) != len(term2.args):
            return None
        for t1, t2 in zip(term1.args, term2.args):
            sust = unificar(t1, t2, sust)
            if sust is None:
                return None
        return sust
    else:
        return None

def unificar_var(var, term, sust):
    if var in sust:
        return unificar(sust[var], term, sust)
    elif occur_check(var, term, sust):
        return None
    else:
        sust[var] = term
        return sust

def occur_check(var, term, sust):
    """Verifica si una variable aparece dentro de un término"""
    if var == term:
        return True
    elif isinstance(term, Function):
        return any(occur_check(var, arg, sust) for arg in term.args)
    elif term in sust:
        return occur_check(var, sust[term], sust)
    return False

# Ejemplo de unificación
print("\nEjemplo de unificación:")
term1 = Q(x, a)
term2 = Q(b, y)
sustitucion = unificar(term1, term2)
print(f"Unificar {term1} con {term2}: {sustitucion}")

# 5. Resolución para lógica de primer orden (versión simplificada)
def resolver_FO(clausulas):
    """Algoritmo de resolución para lógica de primer orden (simplificado)"""
    nuevas = set()
    
    for c1 in clausulas:
        for c2 in clausulas:
            if c1 != c2:
                for lit1 in c1:
                    for lit2 in c2:
                        # Buscar literales complementarios
                        if (isinstance(lit1, Not) and lit1.args[0] == lit2:
                            resolvente = c1.union(c2) - {lit1, lit2}
                            if not resolvente:  # Clausula vacía
                                return True  # Contradicción encontrada
                            nuevas.add(frozenset(resolvente))
                        elif (isinstance(lit2, Not) and lit2.args[0] == lit1:
                            resolvente = c1.union(c2) - {lit1, lit2}
                            if not resolvente:  # Clausula vacía
                                return True  # Contradicción encontrada
                            nuevas.add(frozenset(resolvente))
    
    if not nuevas:
        return False  # No se puede inferir más
    
    # Verificar si las nuevas cláusulas ya estaban presentes
    if nuevas.issubset(clausulas):
        return False
    
    return resolver_FO(clausulas.union(nuevas))

# Ejemplo de resolución
print("\nEjemplo de resolución:")
clausula1 = {P(x), Q(y)}
clausula2 = {Not(P(a))}
clausula3 = {Not(Q(b))}

print("Cláusulas iniciales:")
print(clausula1)
print(clausula2)
print(clausula3)

print("\nResultado de resolución:", resolver_FO({frozenset(clausula1), frozenset(clausula2), frozenset(clausula3)}))

# 6. Base de conocimientos simple
class BaseConocimientos:
    def __init__(self):
        self.hechos = set()
        self.reglas = []
    
    def agregar_hecho(self, hecho):
        self.hechos.add(hecho)
    
    def agregar_regla(self, regla):
        self.reglas.append(regla)
    
    def consultar(self, query):
        """Motor de inferencia simple (encadenamiento hacia adelante)"""
        nuevos_hechos = set()
        
        while True:
            tamanio_inicial = len(self.hechos)
            
            # Aplicar reglas
            for antecedente, consecuente in self.reglas:
                if all(ant in self.hechos for ant in antecedente):
                    nuevos_hechos.add(consecuente)
            
            # Agregar nuevos hechos
            self.hechos.update(nuevos_hechos)
            nuevos_hechos.clear()
            
            # Verificar si se estabilizó
            if len(self.hechos) == tamanio_inicial:
                break
        
        return query in self.hechos

# Ejemplo de base de conocimientos
print("\nBase de conocimientos:")
bc = BaseConocimientos()
bc.agregar_hecho(P(a))
bc.agregar_regla(({P(x)}, Q(x)))
bc.agregar_regla(({Q(x)}, R(x)))

print("¿R(a)?", bc.consultar(R(a)))
print("Hechos finales:", bc.hechos)