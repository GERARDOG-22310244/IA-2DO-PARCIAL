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
gamma = 0.9
theta = 0.01

# Inicializar utilidades y política
utilities = {s: 0 for s in states}
policy = {s: 'ir_a_B' for s in states if s in actions and actions[s]}

def policy_evaluation():
    global utilities
    while True:
        delta = 0
        new_utilities = utilities.copy()
        for s in states:
            if s in policy:
                a = policy[s]
                s_prime = actions[s][a]
                u = rewards[s] + gamma * utilities[s_prime]
                new_utilities[s] = u
                delta = max(delta, abs(new_utilities[s] - utilities[s]))
        utilities = new_utilities
        if delta < theta:
            break

def policy_improvement():
    stable = True
    for s in states:
        if s not in actions or not actions[s]:
            continue
        old_action = policy[s]
        best_action = max(actions[s], key=lambda a: rewards[s] + gamma * utilities[actions[s][a]])
        policy[s] = best_action
        if old_action != best_action:
            stable = False
    return stable

def policy_iteration():
    while True:
        policy_evaluation()
        if policy_improvement():
            break

policy_iteration()

print("🔍 Política óptima:")
for s in policy:
    print(f"Estado {s}: {policy[s]}")
