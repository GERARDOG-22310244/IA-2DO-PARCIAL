# Probabilidades
P_A = 0.01               # Probabilidad de tener la enfermedad (a priori)
P_not_A = 1 - P_A        # Probabilidad de NO tener la enfermedad
P_B_given_A = 0.99       # Sensibilidad: P(Test positivo | Enfermedad)
P_B_given_not_A = 0.05   # Falsos positivos: P(Test positivo | No enfermedad)

# Probabilidad total del test positivo: P(B)
P_B = (P_B_given_A * P_A) + (P_B_given_not_A * P_not_A)

# Regla de Bayes: P(A | B)
P_A_given_B = (P_B_given_A * P_A) / P_B

# Resultado
print(f"P(Test positivo) = {P_B:.4f}")
print(f"P(Enfermedad | Test positivo) = {P_A_given_B:.4f}")
