import numpy as np

# Definición de probabilidades condicionales
P_A = {True: 0.3, False: 0.7}
P_B_given_A = {True: {True: 0.8, False: 0.2}, False: {True: 0.1, False: 0.9}}
P_C_given_A_B = {
    (True, True): {True: 0.99, False: 0.01},
    (True, False): {True: 0.9, False: 0.1},
    (False, True): {True: 0.9, False: 0.1},
    (False, False): {True: 0.0, False: 1.0}
}

def sample_from_distribution(dist):
    return np.random.rand() < dist[True]

def likelihood_weighting(evidence, N):
    weights = {True: 0.0, False: 0.0}
    
    for _ in range(N):
        weight = 1.0
        
        # Sample A (no evidencia en A)
        A = sample_from_distribution(P_A)
        
        # Sample B (no evidencia en B)
        B = sample_from_distribution(P_B_given_A[A])
        
        # Para la evidencia C = True, calcular peso
        if 'C' in evidence:
            c_val = evidence['C']
            weight *= P_C_given_A_B[(A, B)][c_val]
        else:
            # Si no hay evidencia, sampleamos C normalmente
            C = sample_from_distribution(P_C_given_A_B[(A, B)])
        
        # Acumular peso para el valor de A
        weights[A] += weight
    
    # Normalizar resultados
    total_weight = weights[True] + weights[False]
    return {k: v / total_weight for k, v in weights.items()}

# Estimar P(A | C=True)
resultado = likelihood_weighting({'C': True}, 10000)

print("Estimación de P(A | C=True) usando Ponderación de Verosimilitud:")
for val, prob in resultado.items():
    print(f"  A={val}: {prob:.4f}")
