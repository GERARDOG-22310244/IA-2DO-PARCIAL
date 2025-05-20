import random

# Estados, acciones, observaciones
states = ['lleno', 'vacio']
actions = ['esperar', 'llenar']
observations = ['sensor_lleno', 'sensor_vacio']

# Transiciones T[s][a] = [(p, s')]
T = {
    'lleno': {
        'esperar': [('lleno', 0.9), ('vacio', 0.1)],
        'llenar': [('lleno', 1.0)]
    },
    'vacio': {
        'esperar': [('vacio', 0.9), ('lleno', 0.1)],
        'llenar': [('lleno', 1.0)]
    }
}

# Observación Z[s'][o] = probabilidad
Z = {
    'lleno': {'sensor_lleno': 0.8, 'sensor_vacio': 0.2},
    'vacio': {'sensor_lleno': 0.3, 'sensor_vacio': 0.7}
}

# Recompensas
R = {
    'lleno': {'esperar': 5, 'llenar': -1},
    'vacio': {'esperar': -1, 'llenar': 2}
}

# Creencia inicial
belief = {'lleno': 0.5, 'vacio': 0.5}

def normalize(belief):
    total = sum(belief.values())
    return {s: b / total for s, b in belief.items()}

def update_belief(belief, action, observation):
    new_belief = {}
    for s_prime in states:
        prob = 0
        for s in states:
            for next_state, p in T[s][action]:
                if next_state == s_prime:
                    prob += belief[s] * p
        new_belief[s_prime] = prob * Z[s_prime][observation]
    return normalize(new_belief)

def choose_action(belief):
    """Política sencilla: elige la acción con mayor recompensa esperada."""
    expected_rewards = {}
    for a in actions:
        expected_rewards[a] = sum(belief[s] * R[s][a] for s in states)
    return max(expected_rewards, key=expected_rewards.get)

# Simulación simple
for t in range(5):
    action = choose_action(belief)
    print(f"\nPaso {t+1}:")
    print(f"Creencia actual: {belief}")
    print(f"Acción elegida: {action}")

    # Simulación de ambiente: elige nuevo estado real
    real_state = random.choices(states, weights=[belief[s] for s in states])[0]
    possible_transitions = T[real_state][action]
    next_state = random.choices([s for s, _ in possible_transitions],
                                weights=[p for _, p in possible_transitions])[0]

    # Simula observación
    observation = random.choices(observations,
                                 weights=[Z[next_state][o] for o in observations])[0]

    print(f"Observación: {observation}")
    belief = update_belief(belief, action, observation)
