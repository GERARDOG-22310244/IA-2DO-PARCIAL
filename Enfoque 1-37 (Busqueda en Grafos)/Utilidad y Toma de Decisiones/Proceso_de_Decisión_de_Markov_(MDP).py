states = ['A', 'B', 'C', 'D']
actions = {
    'A': ['ir_B', 'ir_C'],
    'B': ['ir_D'],
    'C': ['ir_D'],
    'D': []
}

# Transiciones: T[s][a] = [(probabilidad, estado siguiente, recompensa)]
T = {
    'A': {
        'ir_B': [(1.0, 'B', 5)],
        'ir_C': [(1.0, 'C', 2)]
    },
    'B': {
        'ir_D': [(1.0, 'D', 10)]
    },
    'C': {
        'ir_D': [(1.0, 'D', 0)]
    },
    'D': {}
}

gamma = 0.9
theta = 0.01

# Inicialización
utilities = {s: 0 for s in states}
policy = {s: None for s in states}

def value_iteration():
    global utilities, policy
    while True:
        delta = 0
        new_utilities = utilities.copy()
        for s in states:
            if s not in actions or not actions[s]:
                continue
            max_utility = float('-inf')
            best_action = None
            for a in actions[s]:
                expected = sum(p * (r + gamma * utilities[s_])
                               for (p, s_, r) in T[s][a])
                if expected > max_utility:
                    max_utility = expected
                    best_action = a
            new_utilities[s] = max_utility
            policy[s] = best_action
            delta = max(delta, abs(max_utility - utilities[s]))
        utilities = new_utilities
        if delta < theta:
            break

value_iteration()

print("🔢 Utilidades:")
for s in utilities:
    print(f"{s}: {utilities[s]:.2f}")
print("\n🧭 Política óptima:")
for s in policy:
    print(f"{s}: {policy[s]}")
