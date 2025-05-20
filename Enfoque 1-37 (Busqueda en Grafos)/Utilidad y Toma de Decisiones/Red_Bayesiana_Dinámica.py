import random

# Estados posibles
states = ["funcionando", "fallando"]
observations = ["normal", "anormal"]

# Probabilidades iniciales
initial_probs = {
    "funcionando": 0.9,
    "fallando": 0.1
}

# Modelo de transición: P(estado_t | estado_{t-1})
transition_model = {
    "funcionando": {"funcionando": 0.85, "fallando": 0.15},
    "fallando": {"funcionando": 0.1, "fallando": 0.9}
}

# Modelo de observación: P(obs_t | estado_t)
observation_model = {
    "funcionando": {"normal": 0.8, "anormal": 0.2},
    "fallando": {"normal": 0.3, "anormal": 0.7}
}

def normalize(dist):
    total = sum(dist.values())
    return {k: v / total for k, v in dist.items()}

def forward(prev_belief, observation):
    # Predicción
    predicted = {}
    for curr_state in states:
        predicted[curr_state] = sum(
            prev_belief[prev_state] * transition_model[prev_state][curr_state]
            for prev_state in states
        )

    # Actualización
    updated = {}
    for state in states:
        updated[state] = predicted[state] * observation_model[state][observation]

    return normalize(updated)

# Simulación de inferencia en línea
belief = initial_probs
print("Creencia inicial:", belief)

# Secuencia de observaciones simuladas
observations_seq = ["normal", "anormal", "anormal", "normal"]

for t, obs in enumerate(observations_seq, 1):
    belief = forward(belief, obs)
    print(f"\nPaso {t}: Observación = {obs}")
    print("Creencia actualizada:", belief)
