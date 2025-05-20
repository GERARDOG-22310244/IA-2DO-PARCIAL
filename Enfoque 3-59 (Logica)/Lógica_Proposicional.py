from sympy.logic.boolalg import to_cnf, Or, And, Not, Equivalent
from sympy.logic.inference import satisfiable
from sympy import symbols

# 1. Definición de símbolos proposicionales
A, B, C = symbols('A B C')

# 2. Operadores lógicos básicos
print("Operadores Lógicos:")
print(f"Negación (¬A): {Not(A)}")
print(f"Conjunción (A ∧ B): {And(A, B)}")
print(f"Disyunción (A ∨ B): {Or(A, B)}")
print(f"Implicación (A → B): {Equivalent(A, B)}")  # Equivalente a ¬A ∨ B
print(f"Equivalencia (A ↔ B): {Equivalent(A, B)}")

# 3. Forma Normal Conjuntiva (CNF)
expresion = Or(And(A, B), C)
cnf = to_cnf(expresion)
print(f"\nExpresión original: {expresion}")
print(f"Forma Normal Conjuntiva: {cnf}")

# 4. Satisfacibilidad
expresion_sat = And(A, Or(Not(A), B))
print("\n¿Es satisfacible la expresión", expresion_sat, "?")
print(satisfiable(expresion_sat))

# 5. Tabla de verdad automática
def tabla_verdad(expresion, variables):
    print(f"\nTabla de verdad para {expresion}:")
    print("|".join(str(v) for v in variables) + "| Resultado")
    print("-"*(len(variables)*3 + 9))
    
    # Generar todas las combinaciones posibles
    for valores in generar_combinaciones(len(variables)):
        sustitucion = dict(zip(variables, valores))
        resultado = expresion.subs(sustitucion)
        print("|".join(str(int(v)) for v in valores) + f"|    {int(resultado)}")

def generar_combinaciones(n):
    """Genera todas las combinaciones de n valores booleanos"""
    if n == 1:
        yield (True,)
        yield (False,)
    else:
        for resto in generar_combinaciones(n-1):
            yield (True,) + resto
            yield (False,) + resto

# Ejemplo de tabla de verdad
tabla_verdad(Or(A, Not(B)), [A, B])

# 6. Resolución proposicional
def resolver(expresion):
    cnf = to_cnf(expresion)
    print(f"\nResolución para {expresion}:")
    print(f"CNF: {cnf}")
    
    # Algoritmo simple de resolución (versión simplificada)
    clausulas = set()
    if isinstance(cnf, And):
        for arg in cnf.args:
            clausulas.add(frozenset(obtener_literales(arg)))
    else:
        clausulas.add(frozenset(obtener_literales(cnf)))
    
    print("\nCláusulas iniciales:")
    for c in clausulas:
        print(set(c))
    
    # Aplicar resolución (versión simplificada)
    nuevas_clausulas = set()
    for c1 in clausulas:
        for c2 in clausulas:
            if c1 != c2:
                resolvente = resolver_clausulas(c1, c2)
                if resolvente is not None:
                    nuevas_clausulas.add(resolvente)
    
    print("\nCláusulas derivadas:")
    for c in nuevas_clausulas:
        print(set(c))
    
    if frozenset() in nuevas_clausulas:
        print("\n¡Contradicción encontrada! La expresión es insatisfacible.")
    else:
        print("\nNo se encontró contradicción. La expresión puede ser satisfacible.")

def obtener_literales(expresion):
    """Extrae literales de una cláusula"""
    if isinstance(expresion, Or):
        return expresion.args
    return (expresion,)

def resolver_clausulas(c1, c2):
    """Aplica la regla de resolución a dos cláusulas"""
    for lit1 in c1:
        for lit2 in c2:
            if lit1 == Not(lit2) or Not(lit1) == lit2:
                nuevo = c1.union(c2) - {lit1, lit2}
                return frozenset(nuevo)
    return None

# Ejemplo de resolución
print("\nEjemplo de resolución proposicional:")
expresion_resolucion = And(Or(A, B), Or(Not(A), C), Or(Not(B), Not(C)))
resolver(expresion_resolucion)