# Probabilidades conocidas o estimadas
P_C = 0.1  # P(C): probabilidad de que alguien tenga gripe

# Probabilidades condicionales
P_A_given_C = 0.8   # Probabilidad de fiebre dado que tiene gripe
P_B_given_C = 0.7   # Probabilidad de dolor de cabeza dado que tiene gripe
P_AB_given_C = 0.56  # Probabilidad de fiebre Y dolor de cabeza dado que tiene gripe

# Verificamos independencia condicional
producto = P_A_given_C * P_B_given_C

# Mostrar resultados
print(f"P(A ∩ B | C) = {P_AB_given_C:.4f}")
print(f"P(A | C) * P(B | C) = {producto:.4f}")

if abs(P_AB_given_C - producto) < 1e-4:
    print("✅ A y B son condicionalmente independientes dado C.")
else:
    print("❌ A y B NO son condicionalmente independientes dado C.")
