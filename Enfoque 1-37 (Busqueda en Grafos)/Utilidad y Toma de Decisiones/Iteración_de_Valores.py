states = ['A', 'B', 'C']
actions = {
    'A': {'ir_a_B': 'B', 'ir_a_C': 'C'},
    'B': {},
    'C': {}
}
rewards = {
    'A': 0,
    'B': 10,
    'C': 5
}
gamma = 0.9  # Factor de descuento
theta = 0.01  # Umbral para convergencia

# Inicializar utilidades en 0
utilities = {s: 0 for s in states}

# Iteración de valores
def value_iteration():
    global utilities
    while True:
        delta = 0
        new_utilities = utilities.copy()
        for s in states:
            if s not in actions or not actions[s]:
                continue
            max_utility = float('-inf')
            for a in actions[s]:
                s_prime = actions[s][a]
                u = rewards[s] + gamma * utilities[s_prime]
                max_utility = max(max_utility, u)
            new_utilities[s] = max_utility
            delta = max(delta, abs(new_utilities[s] - utilities[s]))
        utilities = new_utilities
        if delta < theta:
            break

value_iteration()

# Mostrar utilidades finales
print("🔍 Utilidades óptimas por estado:")
for s in states:
    print(f"Estado {s}: {utilities[s]:.2f}")
