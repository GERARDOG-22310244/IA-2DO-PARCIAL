from pgmpy.models import BayesianNetwork
from pgmpy.factors.discrete import TabularCPD
from pgmpy.inference import VariableElimination

# Definir la estructura de la red
modelo = BayesianNetwork([("Gripe", "Fiebre"), ("Gripe", "DolorCabeza")])

# Tablas de probabilidad condicional (CPD)
cpd_gripe = TabularCPD(variable="Gripe", variable_card=2, values=[[0.9], [0.1]])  # P(Gripe): No, Sí

cpd_fiebre = TabularCPD(
    variable="Fiebre", variable_card=2,
    values=[[0.9, 0.2],  # P(Fiebre=No | Gripe=No, Sí)
            [0.1, 0.8]], # P(Fiebre=Sí | Gripe=No, Sí)
    evidence=["Gripe"], evidence_card=[2]
)

cpd_dolor = TabularCPD(
    variable="DolorCabeza", variable_card=2,
    values=[[0.7, 0.1],   # P(Dolor=No | Gripe=No, Sí)
            [0.3, 0.9]],  # P(Dolor=Sí | Gripe=No, Sí)
    evidence=["Gripe"], evidence_card=[2]
)

# Agregar CPDs al modelo
modelo.add_cpds(cpd_gripe, cpd_fiebre, cpd_dolor)

# Verificar validez del modelo
print("¿El modelo es válido?", modelo.check_model())

# Inferencia
inferencia = VariableElimination(modelo)

# Consulta: P(Gripe | Fiebre=Sí, DolorCabeza=Sí)
resultado = inferencia.query(variables=["Gripe"],
                              evidence={"Fiebre": 1, "DolorCabeza": 1})

print("\nP(Gripe | Fiebre=Sí, DolorCabeza=Sí):")
print(resultado)
