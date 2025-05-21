# Probabilidades base
P_A = 0.3
P_not_A = 1 - P_A

P_B_given_A = 0.9
P_B_given_not_A = 0.1

# P(C | A, B)
P_C_given_A_B = 0.8
P_C_given_A_not_B = 0.3
P_C_given_not_A_B = 0.5
P_C_given_not_A_not_B = 0.1

# Usamos la Regla de la Cadena: P(A, B, C) = P(A) * P(B|A) * P(C|A,B)
P_A_B_C = P_A * P_B_given_A * P_C_given_A_B

# También calculamos las demás combinaciones si queremos la distribución completa
P_A_B_notC = P_A * P_B_given_A * (1 - P_C_given_A_B)
P_A_notB_C = P_A * (1 - P_B_given_A) * P_C_given_A_not_B
P_notA_B_C = P_not_A * P_B_given_not_A * P_C_given_not_A_B

# Resultado
print(f"P(A, B, C) = {P_A_B_C:.4f}")
print(f"P(A, B, ¬C) = {P_A_B_notC:.4f}")
print(f"P(A, ¬B, C) = {P_A_notB_C:.4f}")
print(f"P(¬A, B, C) = {P_notA_B_C:.4f}")
