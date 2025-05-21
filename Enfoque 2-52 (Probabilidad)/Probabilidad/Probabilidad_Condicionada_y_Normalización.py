# Probabilidades dadas
P_E = 0.7           # P(E): probabilidad de estudiar
P_no_E = 0.3        # P(¬E): probabilidad de no estudiar
P_A_given_E = 0.9   # P(A | E): probabilidad de aprobar si estudia
P_A_given_no_E = 0.2  # P(A | ¬E): probabilidad de aprobar si no estudia

# 1. Probabilidad total de aprobar: P(A)
P_A = (P_E * P_A_given_E) + (P_no_E * P_A_given_no_E)

# 2. Probabilidad condicionada inversa: P(E | A) usando Teorema de Bayes
P_E_given_A = (P_A_given_E * P_E) / P_A

# 3. Normalización (para obtener P(E | A) y P(¬E | A))
# Obtenemos numeradores
num_E = P_A_given_E * P_E
num_no_E = P_A_given_no_E * P_no_E
# Suma total (denominador para normalización)
normalizador = num_E + num_no_E
# Probabilidades normalizadas
P_E_given_A_norm = num_E / normalizador
P_no_E_given_A_norm = num_no_E / normalizador

# Resultados
print(f"1. P(A) = {P_A:.4f}")
print(f"2. P(E | A) = {P_E_given_A:.4f}")
print("3. Normalización:")
print(f"   P(E | A) normalizado = {P_E_given_A_norm:.4f}")
print(f"   P(¬E | A) normalizado = {P_no_E_given_A_norm:.4f}")
