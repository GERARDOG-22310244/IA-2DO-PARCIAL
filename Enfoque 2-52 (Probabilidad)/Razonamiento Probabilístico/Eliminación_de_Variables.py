from pgmpy.models import BayesianNetwork
from pgmpy.factors.discrete import TabularCPD
from pgmpy.inference import VariableElimination

# Definir estructura de la red
modelo = BayesianNetwork([('A', 'C'), ('B', 'C')])

# Definir CPDs
cpd_A = TabularCPD(variable='A', variable_card=2, values=[[0.7], [0.3]])  # P(A)
cpd_B = TabularCPD(variable='B', variable_card=2, values=[[0.6], [0.4]])  # P(B)

cpd_C = TabularCPD(
    variable='C', variable_card=2,
    values=[
        # C=No: filas
        [1.0, 0.1, 0.1, 0.01],  
        # C=Sí: filas
        [0.0, 0.9, 0.9, 0.99]
    ],
    evidence=['A', 'B'],
    evidence_card=[2, 2]
)

# Añadir CPDs al modelo
modelo.add_cpds(cpd_A, cpd_B, cpd_C)

# Verificar modelo
assert modelo.check_model(), "Modelo inválido"

# Crear objeto para inferencia
inferencia = VariableElimination(modelo)

# Calcular P(A | C=1) con eliminación de variables
resultado = inferencia.query(variables=['A'], evidence={'C': 1})

print("P(A | C=True):")
print(resultado)
