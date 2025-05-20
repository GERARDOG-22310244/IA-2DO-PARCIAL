# Probabilidad de lluvia
P_lluvia = 0.3

# Utilidades (decisión, evento)
utilidades = {
    ('llevar', 'lluvia'): 5,
    ('llevar', 'no_lluvia'): 2,
    ('no_llevar', 'lluvia'): -10,
    ('no_llevar', 'no_lluvia'): 10
}

# Función para utilidad esperada sin información adicional
def utilidad_sin_info():
    decisiones = ['llevar', 'no_llevar']
    def ue(decision):
        return (P_lluvia * utilidades[(decision, 'lluvia')] +
                (1 - P_lluvia) * utilidades[(decision, 'no_lluvia')])
    return max(ue(d) for d in decisiones)

# Función para utilidad esperada con información perfecta
def utilidad_con_info():
    # Si se sabe que lloverá
    decision_lluvia = max(['llevar', 'no_llevar'],
                          key=lambda d: utilidades[(d, 'lluvia')])
    utilidad_lluvia = utilidades[(decision_lluvia, 'lluvia')]
    
    # Si se sabe que no lloverá
    decision_no_lluvia = max(['llevar', 'no_llevar'],
                             key=lambda d: utilidades[(d, 'no_lluvia')])
    utilidad_no_lluvia = utilidades[(decision_no_lluvia, 'no_lluvia')]

    # Utilidad esperada considerando información perfecta
    return (P_lluvia * utilidad_lluvia + (1 - P_lluvia) * utilidad_no_lluvia)

# Cálculo del VOI
ue_sin_info = utilidad_sin_info()
ue_con_info = utilidad_con_info()
valor_info = ue_con_info - ue_sin_info

# Resultados
print(f"Utilidad esperada sin información: {ue_sin_info}")
print(f"Utilidad esperada con información perfecta: {ue_con_info}")
print(f"\n🔍 Valor de la Información: {valor_info}")
