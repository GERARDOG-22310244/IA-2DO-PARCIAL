import random

# Probabilidad de lluvia
P_lluvia = 0.3

# Utilidades:
# (decisión, evento) -> utilidad
utilidades = {
    ('llevar', 'lluvia'): 5,     # Lleva paraguas y llueve
    ('llevar', 'no_lluvia'): 2,  # Lleva paraguas y no llueve (incomodidad)
    ('no_llevar', 'lluvia'): -10, # No lo lleva y llueve (se moja)
    ('no_llevar', 'no_lluvia'): 10 # No lo lleva y no llueve (comodidad)
}

# Calcula utilidad esperada para una decisión
def utilidad_esperada(decision):
    ue = (
        P_lluvia * utilidades[(decision, 'lluvia')] +
        (1 - P_lluvia) * utilidades[(decision, 'no_lluvia')]
    )
    return ue

# Evaluar decisiones
decisiones = ['llevar', 'no_llevar']
for d in decisiones:
    ue = utilidad_esperada(d)
    print(f"Utilidad esperada al decidir '{d}': {ue}")

# Decisión óptima
mejor = max(decisiones, key=utilidad_esperada)
print(f"\n✅ Decisión óptima: '{mejor.upper()}' (máxima utilidad esperada)")
