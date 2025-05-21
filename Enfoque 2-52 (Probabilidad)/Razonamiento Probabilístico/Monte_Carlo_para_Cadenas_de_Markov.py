import numpy as np
import matplotlib.pyplot as plt

def distrib_objetivo(x):
    # Distribución objetivo (densidad no normalizada)
    return np.exp(-x**2 / 2)

def metropolis_hastings(init, n_samples, proposal_width=1.0):
    samples = []
    x = init
    
    for _ in range(n_samples):
        # Propuesta
        x_propuesta = np.random.normal(x, proposal_width)
        
        # Razón de aceptación
        acept_prob = min(1, distrib_objetivo(x_propuesta) / distrib_objetivo(x))
        
        # Decisión de aceptación
        if np.random.rand() < acept_prob:
            x = x_propuesta
        
        samples.append(x)
    return np.array(samples)

# Parámetros
n_muestras = 10000
inicio = 0.0

# Generar muestras con MCMC
muestras = metropolis_hastings(inicio, n_muestras)

# Graficar histogramas
x = np.linspace(-4, 4, 1000)
plt.plot(x, (1/np.sqrt(2*np.pi))*np.exp(-x**2/2), label='Distribución Normal estándar')
plt.hist(muestras, bins=50, density=True, alpha=0.5, label='Muestras MCMC')
plt.legend()
plt.title('Muestreo MCMC con Metropolis-Hastings')
plt.show()
